'''
Created on Feb 9, 2013

@author: mdiamond
'''

import re
from crawling.checker import basic

class Doer:
    def __init__(self):
        pass
    
    def findClass(self, cls):
        def find(url, soup):
            for t in soup.find_all(True,{'class': cls}):
                print(url+":"+str(t))
        return find
    
    def findLink(self, string):
        def func(url, soup):
            for a in soup.findAll('a'):
                if a.has_key('href') and string in a['href']:
                    print('Found link to %s in %s' % (a['href'], url))
        return func
    
    def findLinkPattern(self, pat):
        pattern = re.compile(pat)
        def func(url, soup):
            for a in soup.findAll('a'):
                if a.has_key('href') and pattern.match(a['href']):
                    print('Found link to %s in %s' % (a['href'], url))
        return func
    
    def findInternalNoFollow(self, checker=basic):
        def func(url, soup):
            for a in soup.findAll('a'):
                if checker.isLocal(url):
                    # worth flagging if rel exists at all, and sometimes people use 'nofollow="nofollow"' instead
                    if a.has_key('rel') or a.has_key('nofollow'):
                        print("Found nofollow to %s from %s" % (a['href'],url))
                        break
        return func
    
    def pageTitleContains(self, pat):
        pattern = re.compile(pat)
        def func(url, soup):
            for title in soup.findAll('title'):
                if pattern.search(title.string) is not None:
                    print('%s => %s' % (url, title.string))
        return func

basic = Doer()