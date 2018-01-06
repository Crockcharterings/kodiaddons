#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
from bs4 import BeautifulSoup
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://onelike.tv'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.channel_groups = None
        self.cost = 888

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        for index, l in enumerate(soup.find_all('a',target='_blank',href=re.compile('\/\S+\.html'))):
            try:
                soup = self.get_soup(self.baseurl + l.get('href'))
                channel_title = research(u'^(.*?) смотреть онлайн',soup.title.string)
                channel_logo = self.baseurl + soup.find('img', title=channel_title).get('src')
                channel_link = soup.find('iframe').get('src')
                group_title = self.get_channel_group(l.get('href'))
                if channel_link:
                    channels.append(dict(
                        title=unicode(channel_title),
                        link=unicode(channel_link),
                        logo=unicode(channel_logo),
                        group=unicode(group_title)
                    ))
                logger.debug('get channel %s', self.baseurl + l.get('href'))
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

    def get_channel_group(self, channel):
        if not self.channel_groups:
            self.channel_groups = {
                u'Общие'           : self.get_url('http://onelike.tv/tsentralnye.html'),
                u'Развлекательные' : self.get_url('http://onelike.tv/razvlekatelnye.html'),
                u'Музыка'          : self.get_url('http://onelike.tv/muzhskie-kanaly.html'),
                u'Спорт'           : self.get_url('http://onelike.tv/sportivnye.html'),
                u'Фильмы'          : self.get_url('http://onelike.tv/kanaly-filmov-i-serialov.html'),
                u'Новостные'       : self.get_url('http://onelike.tv/novostnye.html'),
                u'Женские'         : self.get_url('http://onelike.tv/zhenskie-kanaly.html'),
                u'Музыка'          : self.get_url('http://onelike.tv/muzykalnye.html'),
                u'Познавательные'  : self.get_url('http://onelike.tv/poznavatelnye.html'),
                u'Детские'         : self.get_url('http://onelike.tv/detskie-kanaly.html'),
            }
        for group in self.channel_groups:
            if channel in repr(self.channel_groups[group]): return group
        return self.urlparse.netloc
