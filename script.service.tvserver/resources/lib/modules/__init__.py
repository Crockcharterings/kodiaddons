#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, re, cookielib, json, codecs
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger(__name__)

def research(pattern, string, g=1):
    m = re.search(unicode(pattern), unicode(string))
    try: return re.search(pattern, string).group(g)
    except: return ''

class TVResourceTemplate(object):
    def __init__(self, baseurl):
        object.__init__(self)
        self.baseurl = baseurl
        self.urlparse = urllib2.urlparse.urlparse(self.baseurl)
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [
            ('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60'),
            ('Accept', 'text/html, application/xml, application/xhtml+xml, */*'),
            ('Accept-Language', 'ru,en;q=0.9')
        ]
        self.cost = 999

    def _get_channels(self):
        return []

    def _get_stream(self, channel):
        return channel.get('link')

    def get_url(self, url, referer=None):
        if referer is None: referer = self.baseurl
        self.opener.addheaders.append(('Referer', referer))
        response = self.opener.open(url)
        data = response.read()
        del self.opener.addheaders[-1]
        return data

    def get_json(self, url, referer=None):
        if referer is None: referer = self.baseurl
        data = json.loads(self.get_url(url, referer))
        return data

    def get_soup(self, url):
        html = self.get_url(url)
        soup = BeautifulSoup(html,"lxml")
        return soup

    def get_channels(self):
        channels = []
        orig = self._get_channels()
        for channel in orig:
            channels.append(dict(
                hash=unicode(abs(hash(unicode(self.urlparse.netloc)+unicode(channel['title'])))),
                title=unicode(channel['title']),
                logo=unicode(channel.get('logo','')),
                link=unicode(channel['link']),
                group=unicode(channel.get('group',self.urlparse.netloc)).upper(),
                cost=self.cost
            ))
        return channels

    def get_stream(self, channel):
        try:
            stream = self._get_stream(channel)
            return stream
        except Exception as e:
            logger.error(repr(e))
