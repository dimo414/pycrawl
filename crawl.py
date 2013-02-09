'''
Created on Feb 9, 2013

@author: mdiamond
'''

from crawling.crawler import Crawler
from crawling import checker, doer

if __name__ == '__main__':
    crawl = Crawler(checker.basic.isLocal, doer.basic.findInternalNoFollow())
    crawl.crawl('http://www.digitalgemstones.com', 2)