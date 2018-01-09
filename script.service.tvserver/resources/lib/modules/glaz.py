#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules import TVResourceTemplate, research
import re, logging
logger = logging.getLogger(__name__)

class TVResource(TVResourceTemplate):
    baseurl = 'https://www.glaz.tv/online-tv/'
    def __init__(self, baseurl=baseurl):
        super(TVResource, self).__init__(baseurl)
        self.cost = 7

    def _get_channels(self):
        channels = []
        soup = self.get_soup(self.baseurl)
        pages = soup.findAll('a', {'class':'js-pager-item'})
        for p in pages:
            soup = self.get_soup(self.urlparse.scheme + '://' + self.urlparse.netloc + p.get('href'))
            for index, t in enumerate(soup.findAll('section', {'class':'list-channel'})):
                try:
                    if t.find('span', {'class':'external-label'}): continue
                    title = t.find('span', {'class':'list-channel-info__name'}).string
                    link = self.urlparse.scheme + '://' + self.urlparse.netloc + t.find('a', {'class':'list-channel__info'}).get('href')
                    logo = self.urlparse.scheme + ':' + t.find('div', {'class':'list-channel-info__logo'}).find('img').get('src')
                    group = self.get_channel_group(t.find('p', {'class':'article-under-text article-under-text-tv-item list-channel-info'}))
                    channels.append(dict(
                        title=unicode(title),
                        link=unicode(link),
                        logo=unicode(logo),
                        group=unicode(group)
                    ))
                    logger.info('get channel %s', link)
                except Exception as e:
                    logger.error('%s:%s - %s', self.urlparse.netloc, index, repr(e)[:50])
        return channels

    def _get_stream(self, channel):
        stream = None
        html = self.get_url(channel['link']).decode('utf8','ignore')
        if 'wmsAuthSign' in html:
            sig = research('var signature = "(.*?)"', html)
            stream = research('url: "(.*?)" \+ signature', html)
            if stream: stream += sig
        elif 'rosshow' in html:
            soup = self._get_soup(html)
            id_ = soup.find('iframe').get('src').replace('//rosshow.ru/iframe/','')
            stream = 'https://live-rmg.cdnvideo.ru/rmg/' + id_ + '_new.sdp/chunklist.m3u8?hls_proxy_host=pub1.rtmp.s01.l.rmg'
        else:
            soup = self._get_soup(html)
            param = soup.find('param', {'name':'flashvars'})
            if param:
                stream = research('file=(.*)', soup.find('param', {'name':'flashvars'}).get('value'))
        return stream

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
