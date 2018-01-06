#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
from bs4 import BeautifulSoup
import re, logging, urllib2
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'https://www.yandex.ru/portal/tvstream_json/channels?locale=ru&from=morda'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 999

    def _get_channels(self):
        channels = []
        data = self.get_json(self.baseurl)
        for index, t in enumerate(data.get('set',[])):
            try:
                if t.get('logo'): logo = 'http:'+t.get('logo')
                else: logo = ''
                channels.append(dict(
                    title=unicode(t.get('title')),
                    link=unicode(t.get('content_url')),
                    logo=unicode(logo)
                ))
            except Exception as e:
                logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        data = self._get_channels()
        index = [d['title'] for d in data].index(channel['title'])
        return data[index]['link']
