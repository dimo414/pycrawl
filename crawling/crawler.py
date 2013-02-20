'''
Created on Feb 9, 2013

@author: mdiamond
'''

import sys, time
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
    def __init__(self, test, action):
        self.hit_urls = set()
        self.max_urls = None
        self.max_hpm = None
        self.user_agent = None
        
        self.resp_handler = None
        self.test = test
        self.action = action
        if not callable(self.test) or not callable(self.action):
            raise Exception("Must pass callable test and action parameters")
    
    def setMaxUrls(self, maxCount):
        self.max_urls = maxCount
        
    def setMaxHitsPerMin(self, max):
        self.max_hpm = max
    
    def setUserAgent(self, ua):
        self.user_agent = ua
    
    def setResponseHandler(self, resp):
        if not callable(resp):
            raise Exception("Must pass callable response handler")
        self.resp_handler = resp
    
    def reset(self):
        self.hit_urls = set()
    
    def crawlAll(self, urls, depth):
        for url in urls:
            self.crawl(url, depth)
    
    def crawlStdIn(self, depth):
        self.crawAll(sys.stdin.readlines(), depth)

    def crawl(self, url, depth):
        startSet = len(self.hit_urls)
        print("Starting crawl of %s" % url,file=sys.stderr)
        sys.stderr.flush()
        self._crawl(url, depth)
        print('Hit %d pages' % (len(self.hit_urls)-startSet), file=sys.stderr)
        sys.stdout.flush()
        sys.stderr.flush()
    
    def _crawl(self, url, depth):
        soup = self.checkUrl(url)
        
        if soup and depth > 0:
            for link in soup.find_all('a'):
                if link.has_key('href'):
                    rel_url = link['href']
                    if(rel_url and self.test(rel_url)):
                        self._crawl(uparse.urljoin(url,rel_url), depth-1)
    
    def checkUrl(self, url):
        second = datetime.now().second
        if second == 0 or second == 30:
            sys.stdout.flush()
            sys.stderr.flush()
            
        if url in self.hit_urls or (self.max_urls and len(self.hit_urls) >= self.max_urls):
            #print("Skipping %s" % url, file=sys.stderr)
            return None
        
        try:
            print("Crawling %s" % url, file=sys.stderr)
            self.hit_urls.add(url)
            response, soup = self.hitUrl(url)
            
            if self.resp_handler:
                self.resp_handler(response)
            
            self.action(url, soup)
            return soup
        except Exception as e:
            print("Failed to crawl/parse %s\n  %s" % (url,e), file=sys.stderr)
            return None
        
    def hitUrl(self, url):
        if self.max_hpm:
            time.sleep(60.0 / self.max_hpm)
        
        headers = {}
        if self.user_agent:
            headers['user-agent'] = self.user_agent
        response, content = http.request(url, headers=headers)
        soup = BeautifulSoup(content)
        return (response, soup)