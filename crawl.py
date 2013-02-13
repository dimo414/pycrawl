'''
Created on Feb 9, 2013

@author: mdiamond
'''

import re
from crawling.crawler import Crawler
from crawling import test, action

if __name__ == '__main__':
    #crawl = Crawler(checker.basic.isLocal, doer.basic.findInternalNoFollow())
    #crawl.crawl('http://www.digitalgemstones.com', 2)
    
    crawl = Crawler(test.basic.isLocal, action.basic.findClass('fancyTitle'))
    crawl.crawl('http://www.digitalgemstones.com/',1)