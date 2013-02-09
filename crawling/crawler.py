'''
Created on Feb 9, 2013

@author: mdiamond
'''

import sys
from datetime import datetime
import urllib.parse as uparse
import httplib2
from bs4 import BeautifulSoup

http = httplib2.Http()

class Crawler:
    def __init__(self, check, do):
        self.hit_urls = set()
        self.max_urls = None
        self.resp_handler = None
        self.check = check
        self.do = do
        if not (self.check and self.do):
            raise Exception("This is not allowed! %s, %s" % (self.check, self.do))
    
    def setResponseHandler(self, resp):
        self.resp_handler = resp
    
    def setMaxUrls(self, maxCount):
        self.max_urls = maxCount
    
    def reset(self):
        self.hit_urls = set()
    
    def crawlAll(self, urls, depth):
        for url in urls:
            self.crawl(url, depth)

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
                    if(rel_url and self.check(rel_url)):
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
            
            self.do(url, soup)
            return soup
        except Exception as e:
            print("Failed to crawl/parse %s\n  %s" % (url,e), file=sys.stderr)
            return None
        
    def hitUrl(self, url):
        response, content = http.request(url)
        soup = BeautifulSoup(content)
        return (response, soup)