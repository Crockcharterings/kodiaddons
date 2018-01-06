#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
from bs4 import BeautifulSoup
import re, logging, urllib2
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'https://www.glaz.tv/online-tv/'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 444

    def _get_channels(self):
        channels = []
        for page in xrange(1, 19):
            soup = self.get_soup('%s%s/' % (self.baseurl, page))
            for index, t in enumerate(soup.find_all('section', class_='list-channel')):
                try:
                    title = t.find('span', class_='list-channel-info__name').string
                    link = self.urlparse.scheme + '://' + self.urlparse.netloc + t.find('a', class_='list-channel__info').get('href')
                    logo = self.urlparse.scheme + ':' + t.find('div', class_='list-channel-info__logo').find('img').get('src')
                    group = self.get_channel_group(t.find('p', class_='article-under-text article-under-text-tv-item list-channel-info'))
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
        #html = self.get_url(channel['link'])
        #logger.info(html)
        #if 'rosshow' in html: logger.info('rosshow')
        #if 'wmsAuthSign' in html: logger.info('wmsAuthSign')
        return u''


    def get_channel_group(self, html):
        group = self.urlparse.netloc
        if u'Обо всем' in unicode(html): group = u'Общие'
        if u'Развлечения' in unicode(html): group = u'Развлекательные'
        if u'Авто' in unicode(html): group = u'Познавательные'
        if u'Спорт' in unicode(html): group = u'Спорт'
        if u'Кино' in unicode(html): group = u'Фильмы и сериалы'
        if u'Новости' in unicode(html): group = u'Новостные'
        if u'Мода' in unicode(html): group = u'Развлекательные'
        if u'Музыка' in unicode(html): group = u'Музыка'
        if u'Познавательное' in unicode(html): group = u'Познавательные'
        if u'Детям' in unicode(html): group = u'Детские'
        if u'Религия' in unicode(html): group = u'Религиозные'
        return group
