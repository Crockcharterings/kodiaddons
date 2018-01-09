#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://tv-only.org'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 13

    def _get_channels(self):
        channels = []
        html = self.get_url(self.baseurl)
        soup = self._get_soup(html.decode('utf8','ignore'))
        for index, l in enumerate(soup.findAll('li',{'class':'item_tv'})):
            try:
                title = l.find('img').get('alt').replace(u'смотреть онлайн','').strip()
                logo = self.baseurl + l.find('img').get('src')
                link = l.find('a').get('href')
                if link:
                    channels.append(dict(
                        title=unicode(title),
                        link=unicode(link),
                        logo=unicode(logo)
                    ))
                logger.info('get channel %s', link)
            except AttributeError:
                pass
            except Exception as e:
                logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        html = self.get_url(channel['link']).decode('utf8','ignore')
        stream = research("var src = \"(.*?)\"",html)
        return stream
