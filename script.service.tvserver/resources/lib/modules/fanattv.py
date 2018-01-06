#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
from bs4 import BeautifulSoup
import re, logging, urllib2
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'http://fanat.tv/channels'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 444

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        for index, g in enumerate(soup.find_all('div', class_='row')):
            try:
                group = self.get_channel_group(g.find('h2').string)
                for a in g.find_all('a'):
                    link = a.get('href')
                    title = a.find('p').string
                    logo = self.urlparse.scheme + '://' + self.urlparse.netloc + '/' + a.find('img').get('src')
                    channels.append(dict(
                        title=unicode(title),
                        link=unicode(link),
                        logo=unicode(logo),
                        group=unicode(group)
                    ))
                    logger.debug('get channel %s', link)
            except Exception as e:
                logger.error('%s:%s - %s', self.urlparse.netloc, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        html = self.get_url(channel['link'])
        stream = research('file:"(.*?)"',html.decode('utf8'))
        return stream

    def get_channel_group(self, group):
        if u'Основные' == group: group = u'Общие'
        elif u'Развлекательные' == group: group = u'Развлекательные'
        elif u'Местные' == group: group = u'Региональные'
        elif u'Спортивные' == group: group = u'Спорт'
        elif u'Фильмы и сериалы' == group: group = u'Фильмы и сериалы'
        elif u'Новостные' == group: group = u'Новостные'
        elif u'Бизнесс' == group: group = u'Познавательные'
        elif u'Музыкальные' == group: group = u'Музыка'
        elif u'Познавательные' == group: group = u'Познавательные'
        elif u'Детские' == group: group = u'Детские'
        else: group = self.urlparse.netloc
        return group
