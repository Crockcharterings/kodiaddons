#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://only-tv.org'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 11

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        for index, l in enumerate(soup.findAll('div',{'class':'popimageslider-item'})):
            try:
                title = l.find('img').get('alt')
                logo = self.baseurl + l.find('img').get('src')
                link = l.find('a').get('href')
                if link.startswith('/'): link = self.baseurl + l.find('a').get('href')
                soup = self.get_soup(link)
                link = soup.find('iframe', {'src':re.compile('.*php$')}).get('src')
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
        html = self.get_url(channel['link'])
        stream = research("file: '(.*?)'",html)
        if not stream: stream = research("file=(.*?m3u8)",html)
        return stream
