'''
Created on Feb 9, 2013

@author:     Michael Diamond
'''

import os, os.path, sys
if sys.version_info < (3, 0):
    sys.stdout.write("PyCrawl is a Python 3 app.  Go upgrade already.")
    sys.exit(1)

import logging
from optparse import OptionParser
from crawling import test, action
from crawling.crawler import Crawler

__version__ = "0.2"

def configure(argv):
    """Parses command-line arguments to configure the crawler, primarily for logging"""
    parser = OptionParser(version="%%prog %s" % __version__, description="a modular Python web crawler")
    parser.add_option("--logdir", dest="log_dir", help="directory to write logs", metavar="DIR", default='.')
    parser.add_option("-r", "--results", action="store_true", dest="print_results", help="print results", default=False)
    parser.add_option("-p", "--pages", action="store_true", dest="print_pages", help="Print pages crawled", default=False)
    
    (opts, _) = parser.parse_args(sys.argv)
    
    if not os.path.exists(opts.log_dir):
      os.mkdir(opts.log_dir)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s\t%(name)s\t%(levelname)s:\t%(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=os.path.join(opts.log_dir, 'pycrawl.full.log'),
                        filemode='w')
    
    logging.getLogger('misconfigured').setLevel(logging.FATAL)
    
    just_message_fmt = logging.Formatter('%(message)s')
    
    page_handler = logging.FileHandler(os.path.join(opts.log_dir, 'pycrawl.pages.log'), 'w')
    page_handler.setFormatter(just_message_fmt)
    page_handler.setLevel(logging.INFO)
    logging.getLogger('page').addHandler(page_handler)
    
    result_handler = logging.FileHandler(os.path.join(opts.log_dir, 'pycrawl.results.log'), 'w')
    result_handler.setFormatter(just_message_fmt)
    result_handler.setLevel(logging.INFO)
    logging.getLogger('result').addHandler(result_handler)
    
    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.WARN)
    err_handler.setFormatter(logging.Formatter('%(name)-10s %(levelname)-8s  %(message)s'))
    logging.getLogger('').addHandler(err_handler)
    
    if opts.print_pages or opts.print_results:
      out_handler = logging.StreamHandler(sys.stdout)
      out_handler.setLevel(logging.INFO)
      out_handler.setFormatter(just_message_fmt)
      if opts.print_pages:
        logging.getLogger('page').addHandler(out_handler)
      if opts.print_results:
        logging.getLogger('result').addHandler(out_handler)

if __name__ == '__main__':
    """Sample crawl application.  Creates a crawler which will crawl local URLs and print URLs with links containing 'California'.
    Specify a custom user agent (Chrome 24 on Win7) and throttle requests to 10 per minute.  Then crawl the English Wikipedia, hitting
    the homepage and all pages linked to from that page, but no deeper."""
    configure(sys.argv)
    
    crawl = Crawler(test.basic.isLocal, action.basic.tagContains('a', 'California'))
    crawl.setUserAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17")
    crawl.setMaxHitsPerMin(10)
    crawl.crawl('http://en.wikipedia.org/wiki/Main_Page',1)
