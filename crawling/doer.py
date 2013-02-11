'''
Created on Feb 9, 2013

@author: mdiamond
'''

import functools, re
from crawling.checker import basic as basic_c

class Doer:
    def __init__(self):
        pass
    
    # TODO create func(url, soup) passable version of soup.findAll
    
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
    
    def findInternalNoFollow(self, checker=basic_c):
        def func(url, soup):
            for a in soup.findAll('a'):
                if a.has_key('href') and checker.isLocal(a['href']):
                    # worth flagging if rel exists at all, and sometimes people use 'nofollow="nofollow"' instead
                    if a.has_key('rel') or a.has_key('nofollow'):
                        print("Found nofollow to %s from %s" % (a['href'],url))
        return func
    
    # http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#The basic find method: findAll(name, attrs, recursive, text, limit, **kwargs)
    def tagContains(self, tag, pat, attrs={}, printTag=False):
        pattern = re.compile(pat) if pat else None
        def func(url, soup):
            for t in soup.findAll(tag, attrs):
                if not pattern or pattern.search(t.string) is not None:
                    print("%s: %s" % (url, (str(t) if printTag else t.string)))
        return func
    
    # TODO use partials
    def findClass(self, cls, printTag=False):
        return self.tagContains(True, None, {'class': cls}, printTag)
    
    def pageTitleContains(self, pat, printTag=False):
        return self.tagContains('title', pat, printTag=printTag)

basic = Doer()