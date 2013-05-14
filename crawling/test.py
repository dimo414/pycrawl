'''
Created on Feb 8, 2013

@author: Michael Diamond
'''
import crawling

class UrlTest:
    """Instances of this class hold a series of methods or
    factory methods used by a Crawler to determine if a given
    URL should be crawled.
    
    Methods expect a URL and return true if the URL should be crawled.
    Factory methods take other parameters, and return a function with the
    above signature.
    
    You can extend this class to implement site specific tests
    or override the existing methods where appropriate, for instance
    if /redirect.php?url=.... is used by a site to send users to external
    sites, you might want to extend isLocal to return false on such URLs."""
    def __init__(self):
        pass
    
    def isLocal(self, url):
        """Only crawl URLs  local to the current host."""
        if url.startswith('//') or url.startswith('mailto'):
            return False
        try:
            if url.index(':') < url.index('/'):
                return False
        except ValueError:
            pass
        return True
    
    def include(self, include):
        """Crawl URLs that contain any of the given strings."""
        include = list(include)
        def func(url):
            return any(s in url for s in include)
        return func
    
    def exclude(self, exclude):
        """Crawl URLs that do not contain any of the given strings."""
        def func(url):
            return not any(s in url for s in exclude)
        return func
    
    def includeLocal(self, include):
        """Crawl local URLs containing any of the given strings."""
        return crawling.checkAll(self.isLocal, self.include(include))
    
    def excludeLocal(self, exclude):
        """Crawl local URLs contianing none of the given strings."""
        return crawling.checkAll(self.isLocal, self.exclude(exclude))
        
basic = UrlTest()