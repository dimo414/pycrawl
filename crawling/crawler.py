'''
Created on Feb 9, 2013

@author: Michael Diamond
'''

import logging, sys, time
from datetime import datetime
import urllib.parse as uparse
import httplib2
from bs4 import BeautifulSoup

# Basic, request-agnostic http crawler
http = httplib2.Http()
# Caching enabled, since Crawler attempts to avoid hitting pages more than once, not terribly useful
#http = httplib2.Http('/tmp/.httplib2_cache')
# Cookies persist between requests, replicates a user session
#http = httplib2.Http(handle_cookies=True)

class Crawler:
    """Crawler instances control a website crawl, making requests against
    the given URLs, performing the specified actions, and notably queuing
    valid lings found on the crawled pages for crawling as well.
    """
    def __init__(self, test, action):
        """test: callable which expects a string URL parameter, and returns
        true if the given URL should be crawled.
        action: callable which expects a string URL and BeautifulSoup page object,
        and performs whatever actions should be done on the page."""
        self.logger = logging.getLogger('crawler')
        self.page = logging.getLogger('page').info
        self.hit_urls = set()
        self.max_urls = None
        self.max_hpm = None
        self.user_agent = None
        
        self.cookies = {}
        self.resp_handler = None
        self.test = test
        self.action = action
        if not callable(self.test) or not callable(self.action):
            raise Exception("Must pass callable test and action parameters")
    
    def setMaxUrls(self, maxCount):
        """If set, crawler will stop crawling once it's visited maxCount pages."""
        self.max_urls = maxCount
        
    def setMaxHitsPerMin(self, max):
        """If set, throttles crawl speed to max requests per minute."""
        self.max_hpm = max
    
    def addCookie(self, name, value):
      """Specify a cookie to be sent with every request"""
      self.cookies[name] = value
    
    def setUserAgent(self, ua):
        """Specifies a user-agent to crawl as.  Uses httplib2's default if not set."""
        self.user_agent = ua
    
    def setResponseHandler(self, resp):
        """Callable which expects an httplib2 response object, useful for checking response
        contents, such as the HTTP response code."""
        if not callable(resp):
            raise Exception("Must pass callable response handler")
        self.resp_handler = resp
    
    def reset(self):
        """Clears the list of visited URLs.  Note that this does not rest the http object's state."""
        self.hit_urls = set()
    
    def crawlAll(self, urls, depth):
        """Given a list of URLs, crawls each to depth in turn."""
        for url in urls:
            self.crawl(url, depth)
    
    def crawlStdIn(self, depth):
        """Passes standard input to crawlAll() - useful for piping a list of URLs into the crawler.
        cat urls.txt | crawl.py"""
        self.crawAll(sys.stdin.readlines(), depth)

    def crawl(self, url, depth):
        """Crawl a given URL to depth.  Visits URL, renders the response
        as a BeautifulSoup soup object, runs crawler action against the page,
        and crawls all unvisited links on page passing the crawler's test at
        depth-1 until depth = 0 or the maximum number of pages has been reached.
        Note that the initial URL is not checked against the crawler's test, only
        URLs found on page are subject to this filter."""
        startSet = len(self.hit_urls)
        self.page("Starting crawl of %s", url)
        sys.stderr.flush()
        self._crawl(url, depth)
        self.page('Hit %d pages', (len(self.hit_urls)-startSet))
        sys.stdout.flush()
        sys.stderr.flush()
    
    def _crawl(self, url, depth):
        """Helper method for crawl(), doesn't write "Starting ..." and "Hit ..."
        messages to standard error."""
        soup = self.checkUrl(url.partition('#')[0]) # avoid anchor URLs
        
        if soup and depth > 0:
            for link in soup.find_all('a'):
                if link.has_key('href'):
                    rel_url = link['href']
                    if(rel_url and self.test(rel_url)):
                        self._crawl(uparse.urljoin(url,rel_url), depth-1)
    
    def checkUrl(self, url):
        """Checks a given URL.
          1. Skip URL if already visited
          2. Visit URL and render BeautifulSoup object
          3. Apply response handler if set
          4. Run crawler's action against the page
          5. Pass soup object up to be inspected for URLs to crawl
        """
        second = datetime.now().second
        if second == 0 or second == 30:
            sys.stdout.flush()
            sys.stderr.flush()
            
        if url in self.hit_urls or (self.max_urls and len(self.hit_urls) >= self.max_urls):
            #self.logger.debug("Skipping %s", url)
            return None
        
        try:
            self.page("Crawling %s", url)
            self.hit_urls.add(url)
            response, soup = self.hitUrl(url)
            
            if self.resp_handler:
                self.resp_handler(response)
            
            self.action(url, soup)
            return soup
        except Exception as e:
            self.logger.warn("Failed to crawl/parse %s\n  %s", url, e)
            return None
        
    def hitUrl(self, url):
        """Makes request to URL, returning response and BeautifulSoup objects.""" 
        if self.max_hpm:
            time.sleep(60.0 / self.max_hpm)
        
        headers = {}
        if self.user_agent:
            headers['user-agent'] = self.user_agent
        if self.cookies:
            headers['cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.cookies.items()])
        response, content = http.request(url, headers=headers)
        soup = BeautifulSoup(content)
        return (response, soup)