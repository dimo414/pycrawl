'''
Created on Feb 9, 2013

@author: mdiamond
'''

import re
from crawling.crawler import Crawler
from crawling import checker, doer

if __name__ == '__main__':
    #crawl = Crawler(checker.basic.isLocal, doer.basic.findInternalNoFollow())
    #crawl.crawl('http://www.digitalgemstones.com', 2)
    
    crawl = Crawler(checker.basic.isLocal, doer.basic.findClass('external'))
    crawl.crawl('http://en.wikipedia.org/wiki/Main_Page',1)