import re
import sys
import time
import math
import urllib2
import urlparse
import optparse
from cgi import escape
from traceback import format_exc
from Queue import Queue, Empty as QueueEmpty
from pprint import pprint

from bs4 import BeautifulSoup


# modified version of a simple web crawler by JamesMills and available at
# http://code.activestate.com/recipes/576551-simple-web-crawler/
# and is under the MIT License

__version__ = "0.2"
__copyright__ = "CopyRight (C) 2008-2011 by James Mills"
__license__ = "MIT"
__author__ = "James Mills"
__author_email__ = "James Mills, James dot Mills st dotred dot com dot au"

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)

class Crawler(object):

    def __init__(self, root, depth, locked=True):
        self.root = root
        self.depth = depth
        self.locked = locked
        self.host = urlparse.urlparse(root)[1]
		#change self.urls into a dictionary
        self.urls = {} 
        self.links = 0
        self.followed = 0

    def crawl(self):
        page = Fetcher(self.root)
        page.fetch()
        self.urls[self.root] = []
        q = Queue()
        for url in page.urls:
            q.put(url)
            #put in each link in the dict value (list of links)
            self.urls[self.root].append(url)
            #self.urls[self.root] = [templist.append(url) for templist in self.urls[self.root]]
        followed = [self.root]

        n = 0

        while True:
            try:
                url = q.get()
            except QueueEmpty:
                break

            n += 1

            if url not in followed:
                try:
                    host = urlparse.urlparse(url)[1]
                    if self.locked and re.match(".*%s" % self.host, host):
                        followed.append(url)
                        self.followed += 1
                        page = Fetcher(url)
                        page.fetch()
                        for i, url_2 in enumerate(page):
                            if not self.urls.has_key(url):
                                #I try to put in the link as an item in the value corresponding to the key
                                self.urls[url] = [url_2]
                            else:
                                self.urls[url].append(url_2)
							#    self.urls[url] = [templist.append(url_2) for templist in self.urls[url]]
                            self.links += 1
                            q.put(url_2)
                        if n > self.depth and self.depth > 0:
                            break
                except Exception, e:
                    print "ERROR: Can't process url '%s' (%s)" % (url, e)
                    print format_exc()

class Fetcher(object):

    def __init__(self, url):
        self.url = url
        self.urls = []

    def __getitem__(self, x):
        return self.urls[x]

    def _addHeaders(self, request):
        request.add_header("User-Agent", AGENT)

    def open(self):
        url = self.url
        try:
            request = urllib2.Request(url)
            handle = urllib2.build_opener()
        except IOError:
            return None
        return (request, handle)

    def fetch(self):
        request, handle = self.open()
        self._addHeaders(request)
        if handle:
            try:
                content = unicode(handle.open(request).read(), "utf-8",
                        errors="replace")
                soup = BeautifulSoup(content)
                tags = soup('a')
            except urllib2.HTTPError, error:
                if error.code == 404:
                    print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
                else:
                    print >> sys.stderr, "ERROR: %s" % error
                tags = []
            except urllib2.URLError, error:
                print >> sys.stderr, "ERROR: %s" % error
                tags = []
            for tag in tags:
                href = tag.get("href")
                if href is not None:
                    url = urlparse.urljoin(self.url, escape(href))
                    if url not in self:
                        self.urls.append(url)

def getLinks(url):
    page = Fetcher(url)
    page.fetch()
    for i, url in enumerate(page):
        print "%d. %s" % (i, url)

def parse_options():
    """parse_options() -> opts, args

    Parse any command-line options given returning both
    the parsed options and arguments.
    """

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-q", "--quiet",
            action="store_true", default=False, dest="quiet",
            help="Enable quiet mode")

    parser.add_option("-l", "--links",
            action="store_true", default=False, dest="links",
            help="Get links for specified url only")

    parser.add_option("-d", "--depth",
            action="store", type="int", default=30, dest="depth",
            help="Maximum depth to traverse")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit, 1

    return opts, args

def main():
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth = opts.depth

    sTime = time.time()

    output_f = open("output.txt", "w+")
	
    print "Crawling %s (Max Depth: %d)" % (url, depth)
    crawler = Crawler(url, depth)
    crawler.crawl()
    pprint(crawler.urls, output_f)

    eTime = time.time()
    tTime = eTime - sTime

    print "Found:    %d" % crawler.links
    print "Followed: %d" % crawler.followed
    print "Stats:    (%d/s after %0.2fs)" % (
            int(math.ceil(float(crawler.links) / tTime)), tTime)

if __name__ == "__main__":
    main()