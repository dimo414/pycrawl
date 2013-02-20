'''
Created on Feb 9, 2013

@author: Michael Diamond
'''

import functools, re
from crawling.test import basic as basic_t

class SoupAction:
    """Instances of this class hold a series of methods or factory
    methods used by a Crawler to inspect and act on a page's contents.
    
    Methods expect a URL and a BeautifulSoup object and carry out whatever
    actions they need to.  Common behavior includes printing information
    to standard output, writing data to a file, or initializing (preferably
    asynchronously) some other behavior, like hitting a DB.
    Factory methods take other parameters, and return a function with the
    above signature.
    
    You can extend this class to implement site specific actions."""
    def __init__(self):
        pass
    
    # TODO create func(url, soup) passable version of soup.findAll
    
    def findLink(self, string):
        """Prints links (and the page they were found on) containing the given string."""
        def func(url, soup):
            for a in soup.findAll('a'):
                if a.has_key('href') and string in a['href']:
                    print('Found link to %s in %s' % (a['href'], url))
        return func
    
    def findLinkPattern(self, pat):
        """Prints links (and the page they were found on) matching the given pattern."""
        pattern = re.compile(pat)
        def func(url, soup):
            for a in soup.findAll('a'):
                if a.has_key('href') and pattern.match(a['href']):
                    print('Found link to %s in %s' % (a['href'], url))
        return func
    
    def findInternalNoFollow(self, checker=basic_t):
        """Looks for internal links (as determined by a UrlTest instance) which
        have been nofollowed, and prints the link and the current URL."""
        def func(url, soup):
            for a in soup.findAll('a'):
                if a.has_key('href') and checker.isLocal(a['href']):
                    # worth flagging if rel exists at all, and sometimes people use 'nofollow="nofollow"' instead
                    if a.has_key('rel') or a.has_key('nofollow'):
                        print("Found nofollow to %s from %s" % (a['href'],url))
        return func
    
    # http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#The basic find method: findAll(name, attrs, recursive, text, limit, **kwargs)
    def tagContains(self, tag, pat, attrs={}, printTag=False):
        """Searches for tags containing the given pattern, and prints
        the URL and the matched contents, or the whole tag if printTag is True.
        
        tag and attrs params are passed to BS's findAll method, and can take any
        appropriate values.  If pattern is not set, all tags match."""
        pattern = re.compile(pat) if pat else None
        def func(url, soup):
            for t in soup.findAll(tag, attrs):
                if not pattern or (t.string and pattern.search(t.string) is not None):
                    print("%s: %s" % (url, (str(t) if printTag else t.string)))
        return func
    
    # TODO use partials
    def findClass(self, cls, printTag=False):
        """Searches for tags with the given class, and prints
        the URL and the matched contents, or the whole tag if printTag is True.
        
        tag and attrs params are passed to BS's findAll method, and can take any
        appropriate values.  If pattern is not set, all tags match."""
        return self.tagContains(True, None, {'class': cls}, printTag)
    
    def pageTitleContains(self, pat):
        """Prints URLs and page title for pages with titles matching the given pattern."""
        return self.tagContains('title', pat)
    
    def _tagPath(self, tag, incIndicies=False):
        '''Helper method returns the path from the document root to this tag.  Useful
        for reporting the path to given tags, or tracking where tags appear on a page.
        
        For instance, the result of this method can be used in a set to check if the matched
        tag has appear in this location before, potentially useful for finding different
        layouts containing the same tag.'''
        def idClassStr(tag):
            '''Given a tag, return a string of it's ID / classes, or the empty string'''
            tId = '#%s' % tag['id'] if tag.has_key('id') else ''
            tClass = '.%s' % '.'.join(tag['class']) if tag.has_key('class') else ''
            return '%s%s' % (tId, tClass)
        # Exclude the root and reverse the parent list so we go from html down to tag
        tagLs = (list(paren for paren in tag.parents if paren.name != '[document]')[::-1]+[tag])
        return ' '.join('%s%s%s' % (elem.name, ':%s' % len(list(elem.previous_siblings)) if incIndicies else '', idClassStr(elem)) for elem in tagLs)

basic = SoupAction()