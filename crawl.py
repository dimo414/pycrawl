'''
Created on Feb 9, 2013

@author:     Michael Diamond
'''

import sys
if sys.version_info < (3, 0):
    sys.stdout.write("PyCrawl is a Python 3 app.  Go upgrade already.")
    sys.exit(1)

import re
from crawling.crawler import Crawler
from crawling import test, action

if __name__ == '__main__':
    """Sample crawl application.  Creates a crawler which will crawl local URLs and print URLs with links containing 'California'.
    Specify a custom user agent (Chrome 24 on Win7) and throttle requests to 10 per minute.  Then crawl the English Wikipedia, hitting
    the homepage and all pages linked to from that page, but no deeper."""
    crawl = Crawler(test.basic.isLocal, action.basic.tagContains('a', 'California'))
    crawl.setUserAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17")
    crawl.setMaxHitsPerMin(10)
    crawl.crawl('http://en.wikipedia.org/wiki/Main_Page',1)