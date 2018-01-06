#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
from bs4 import BeautifulSoup
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://tv-torrent.info/ttv.json'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 333

    def _get_channels(self):
        channels = []
        data = eval(self.get_url(self.baseurl))
        for index, l in enumerate(data['channels']):
            try:
                channel_title = l['name'].decode('utf8')
                channel_link = ''.join(['/ace/getstream?id=',l['url'],'&.mp4'])
                group_title = l['cat'].decode('utf8')
                channels.append(dict(
                    title=unicode(channel_title),
                    link=unicode(channel_link),
                    group=unicode(group_title)
                ))
            except Exception as e:
                logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        data = eval(self.get_url(self.baseurl))['channels']
        index = [d['name'].decode('utf8') for d in data].index(channel['title'])
        return ''.join(['/ace/getstream?id=',data[index]['url'],'&.mp4'])
