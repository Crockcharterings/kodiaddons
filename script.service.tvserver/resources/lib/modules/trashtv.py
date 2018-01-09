#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging, json
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://pomoyka.lib.emergate.net/trash/ttv-list/ttv.json'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 1

    def _get_channels(self):
        channels = []
        data = self.get_url(self.baseurl).replace('\n','').strip().decode("utf-8-sig")
        data = json.loads(data)
        for index, l in enumerate(data['channels']):
            try:
                title = l['name']
                link = ''.join(['/ace/getstream?id=',l['url'],'&.mp4'])
                group = l['cat']
                channels.append(dict(
                    title=unicode(title),
                    link=unicode(link),
                    group=unicode(group)
                ))
                logger.info('get channel %s', link)
            except Exception as e:
                logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        data = self.get_url(self.baseurl).replace('\n','').strip().decode("utf-8-sig")
        data = json.loads(data)['channels']
        index = [d['name'] for d in data].index(channel['title'])
        return ''.join(['/ace/getstream?id=',data[index]['url'],'&.mp4'])
