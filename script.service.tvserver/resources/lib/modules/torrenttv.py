#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
from bs4 import BeautifulSoup
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://torrent-tv.ru/channels.php'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 333

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        base = self.urlparse.scheme+'://'+self.urlparse.netloc
        groups = soup.find_all('a', class_='cat-link')
        divs = soup.find_all('div', class_='best-channels')
        for index, group in enumerate(groups):
            for d in divs[index].find_all('div', class_='best-channels-content'):
                try:
                    channel_link = d.find('h5').find('a').get('href')+'&engine=acestream'
                    channel_title = d.find('strong').string.strip()
                    channel_logo = base + '/' + d.find('img').get('src')
                    group_title = group.string.strip()
                    channels.append(dict(
                        title=unicode(channel_title),
                        link=unicode(channel_link),
                        channel_logo=unicode(channel_logo),
                        group=unicode(group_title)
                    ))
                except Exception as e:
                    logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        soup = self.get_soup(channel['link'])
        ttvp = soup.find('div', id='ttv-player')
        if 'cdn/0_' in ttvp: return
        return '/ace/getstream?url=' + ttvp.get('data-stream_url')
