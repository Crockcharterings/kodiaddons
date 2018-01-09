#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://allfon-tv.com'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 10

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        for index, l in enumerate(soup.findAll('figure', {'class':'img'})):
            try:
                title = l.find('figcaption').string.strip()
                link = self.baseurl + l.find('a').get('href')
                logo = self.baseurl + l.find('img').get('src')
                channels.append(dict(
                    title=unicode(title),
                    link=unicode(link),
                    logo=unicode(logo)
                ))
                logger.info('get channel %s', link)
            except Exception as e:
                logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        html = self.get_url(channel['link'])
        stream = research("acestream://(.*?)\"",html.decode('utf8'))
        return '/ace/getstream?id=' + stream
