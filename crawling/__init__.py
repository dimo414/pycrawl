'''
Created on Feb 9, 2013

@author: Michael Diamond
'''

#
# Function combinators
#

def doAll(*funcs):
    """Takes a set of functions and returns a function
    which calls each function in turn, with the passed parameters."""
    def dAll(*args, **opts):
        for func in funcs:
            func(*args, **opts)
    return dAll

def checkAll(*funcs):
    """Takes a set of functions and calls each function in turn,
    returning True if all functions returned true."""
    def cAll(*args, **opts):
        ret = True
        for func in funcs:
            ret= ret and func(*args, **opts)
        return ret
    return cAll

def checkAny(*funcs):
    """Takes a set of functions and calls each function in turn,
    returning True if any function returned true."""
    def cAny(*args, **opts):
        ret = False
        for func in funcs:
            ret = ret or func(*args, **opts)
        return ret
    return cAny

def negate(func):
    """Calls the passed boolean function and returns it's negation."""
    def neg(*args, **opts):
        return not func(*args, **opts)
    return neg

#
# Response Handlers expect a Response object.
#

def failOnError(resp):
    """Common response handler to deal with error pages.  Raises an exception, which
    prevents the page from being parsed, stops the crawler from proceeding any deeper,
    (without interrupting the rest of the crawl) and prints that the page failed."""
    if resp.status != 200:
        raise Exception()
        