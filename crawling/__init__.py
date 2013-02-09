'''
Created on Feb 9, 2013

@author: mdiamond
'''

def doAll(*funcs):
    def dAll(*args, **opts):
        for func in funcs:
            func(*args, **opts)
    return dAll

def checkAll(*funcs):
    def cAll(*args, **opts):
        ret = True
        for func in funcs:
            ret= ret and func(*args, **opts)
        return ret
    return cAll

def checkAny(*funcs):
    def cAny(*args, **opts):
        ret = False
        for func in funcs:
            ret = ret or func(*args, **opts)
        return ret
    return cAny

def negate(func):
    def neg(*args, **opts):
        return not func(*args, **opts)
    return neg

#
# Response Handlers expect a Response object.
#

# Raising an exception stops page parsing and doesn't crawl children, printing an error.
def failOnError(resp):
    if resp.status != 200:
        raise Exception()