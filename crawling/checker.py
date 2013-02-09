'''
Created on Feb 8, 2013

@author: mdiamond
'''
import crawling

class Checker:
    def __init__(self):
        pass
    
    def isLocal(self, url):
        try:
            if url.index(':') < url.index('/'):
                return False
        except:
            pass
        return True
    
    def include(self, include):
        def func(url):
            return any(s in url for s in include)
        return func
    
    def exclude(self, exclude):
        def func(url):
            return not any(s in url for s in exclude)
        return func
    
    def includeLocal(self, include):
        return crawling.checkAll(self.isLocal, self.include)
    
    def excludeLocal(self, exclude):
        return crawling.checkAll(self.isLocal, self.exclude)
        
basic = Checker()