#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://ok-tv.org'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 5

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        for index, a in enumerate(soup.findAll('a', {'class':'bt-image-link'})):
            try:
                title = re.sub(u'(С|с)мотреть\s+онлайн.*$',u'',a.get('title'),flags=re.I).strip()
                logo = self.baseurl + a.find('img').get('src')
                soup = self.get_soup(self.baseurl + a.get('href'))
                link = soup.find('iframe').get('src')
                channels.append(dict(
                    title=unicode(title),
                    link=unicode(link),
                    logo=unicode(logo)
                ))
                logger.info('get channel %s', self.baseurl + a.get('href'))
            except AttributeError:
                pass
            except Exception as e:
                logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        html = self.get_url(channel['link'])
        stream = research("file: '(.*?)'",html.decode('utf8'))
        return stream
