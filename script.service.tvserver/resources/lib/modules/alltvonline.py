#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging, base64
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://www.alltvonline.ru/api/channels?language_id=2'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 9

    def _get_channels(self):
        channels = []
        data = self.get_json(self.baseurl)
        for index, l in enumerate(data['channels']):
            try:
                title = l['name']
                link = ''.join([self.urlparse.scheme,'://',self.urlparse.netloc,'/channel/',l['url']])
                logo = ''.join([self.urlparse.scheme,'://',self.urlparse.netloc,'/data/channels/',l['url']])
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
        stream = research("var m_link = '(.*?)'",html.decode('utf8'))
        stream = base64.decodestring(stream)
        if 'tvrec' in stream: return
        if 'peers' in stream: return
        return stream
