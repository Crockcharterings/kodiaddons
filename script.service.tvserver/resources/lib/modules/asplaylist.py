#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging, urllib2, ssl
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://www.trambroid.com/playlist.xspf'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 4

    def get_url(self, url, referer=None):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request, context=ssl._create_unverified_context())
        data = response.read()
        return data

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        for index, t in enumerate(soup.findAll('track')):
            try:
                title = t.find('title').string.strip()
                link = '/ace/getstream?url=' + t.find('location').string.strip()
                channels.append(dict(
                    title=unicode(title),
                    link=unicode(link)
                ))
                logger.debug('get channel %s', t.find('location').string.strip())
            except Exception as e:
                logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        data = self._get_channels()
        index = [d['title'] for d in data].index(channel['title'])
        return data[index]['link']
