#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://torrent-tv.ru/channels.php'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 3

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        base = self.urlparse.scheme+'://'+self.urlparse.netloc
        groups = soup.findAll('a', {'class':'cat-link'})
        divs = soup.findAll('div', {'class':'best-channels'})
        for index, g in enumerate(groups):
            for d in divs[index].findAll('div', {'class':'best-channels-content'}):
                try:
                    link = d.find('h5').find('a').get('href')+'&engine=acestream'
                    title = d.find('strong').string.strip()
                    logo = base + '/' + d.find('img').get('src')
                    group = g.string.strip()
                    channels.append(dict(
                        title=unicode(title),
                        link=unicode(link),
                        logo=unicode(logo),
                        group=unicode(group)
                    ))
                    logger.info('get channel %s', link)
                except Exception as e:
                    logger.error('%s:%s - %s', self.baseurl, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        soup = self.get_soup(channel['link'])
        ttvp = soup.find('div', {'id':'ttv-player'})
        if 'cdn/0_' in ttvp: return
        return '/ace/getstream?url=' + ttvp.get('data-stream_url')
