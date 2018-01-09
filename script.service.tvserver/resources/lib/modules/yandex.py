#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'https://www.yandex.ru/portal/tvstream_json/channels?locale=ru&from=morda'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 15

    def _get_channels(self):
        channels = []
        data = self.get_json(self.baseurl)
        for index, t in enumerate(data.get('set',[])):
            try:
                if t.get('logo'): logo = 'http:'+t.get('logo')
                else: logo = ''
                title = t.get('title')
                link = t.get('content_url')
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
        data = self.get_json(self.baseurl)
        index = [d['title'] for d in data.get('set',[])].index(channel['title'])
        return data[index]['link']
