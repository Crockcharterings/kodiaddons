#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, logging, json, codecs, urllib2, requests, ssl, imp, importlib, time, subprocess, re
import xbmcaddon, xbmc
from datetime import datetime, timedelta
import sqlite3

logger = logging.getLogger(__name__)
addon = xbmcaddon.Addon()
DB = os.path.join(addon.getAddonInfo('path'),'resources','database.db')

#open = codecs.open
#def u(x):
#    return codecs.unicode_escape_decode(x)[0]

class Channels(object):
    def __init__(self):
        object.__init__(self)

    def _request(self, url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, context=ssl._create_unverified_context())
            data = response.read()
            return data
        except: pass

    def update_channels(self):
        conn = sqlite3.connect(DB)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        file, pathname, description = imp.find_module('modules')
        if file:
            logger.critical('Not a package: modules')
            return
        for module in os.listdir(pathname):
            if module.endswith('.py') and not module.startswith('__') and 'fanattv' in module:
                try:
                    logger.info('update channels from module %s', module)
                    mod = importlib.import_module('modules.'+module[:-3])
                    resource = mod.TVResource()
                    channels = resource.get_channels()
                    resource_hash = abs(hash(resource.urlparse.netloc))
                    channels_db = conn.cursor().execute("""
                        select * from channels_orig
                        where resource_hash = {0}""".format(resource_hash)).fetchall()
                    for channel in channels:
                        item = channels_db.loc[channels_db['hash'] == channel['hash']]
                        if not item.empty:
                            item = item.to_dict(orient='record')[0]
                            if item['resource'] != module:
                                logger.info('update channel %s resource', channel['title'])
                                conn.cursor().execute("""
                                    update channels_orig set resource = ?, timestamp = ?
                                    where hash = ? and resource_hash = ?""",
                                    (module, int(time.time()-time.mktime(time.gmtime(0))), channel['hash'], resource_hash))
                                conn.commit()
                            if item['link'] != channel['link']:
                                logger.info('update channel %s link %s', channel['title'], channel['link'])
                                conn.cursor().execute("""
                                    update channels_orig set link = ?, timestamp = ?
                                    where hash = ? and resource_hash = ?""",
                                    (channel['link'], int(time.time()-time.mktime(time.gmtime(0))), channel['hash'], resource_hash))
                                conn.commit()
                            if item['logo'] != channel['logo']:
                                logger.info('update channel %s logo %s', channel['title'], channel['logo'])
                                conn.cursor().execute("""
                                    update channels_orig set logo = ?, timestamp = ?
                                    where hash = ? and resource_hash = ?""",
                                    (channel['logo'], int(time.time()-time.mktime(time.gmtime(0))), channel['hash'], resource_hash))
                                conn.commit()
                            if item['cost'] != channel['cost']:
                                logger.info('update channel %s cost %s', channel['title'], channel['cost'])
                                conn.cursor().execute("""
                                    update channels_orig set cost = ?, timestamp = ?
                                    where hash = ? and resource_hash = ?""",
                                    (channel['cost'], int(time.time()-time.mktime(time.gmtime(0))), channel['hash'], resource_hash))
                                conn.commit()
                        else:
                            logger.info('add channel %s', channel['title'])
                            conn.cursor().execute("""
                                insert into channels_orig (
                                resource, resource_hash, hash, title, logo, link, group_, cost, timestamp)
                                values (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (module, resource_hash, channel['hash'], channel['title'], channel['logo'],
                                 channel['link'], channel['group'], channel['cost'],
                                 int(time.time()-time.mktime(time.gmtime(0)))))
                            conn.commit()
                except Exception as e:
                    logger.error('%s: %s', module, repr(e))
        conn.close()

    def update_channel(self, ch_name, gr_name, channel_title, group_title):
        conn = sqlite3.connect(DB)
        try:
        	conn.cursor().execute("""
        		update channels_names set name = ?
        		where name = ?""",
        		(channel_title, ch_name))
        	conn.commit()
        	conn.cursor().execute("""
        		update channels_groups set group_title = ?
        		where group_title = ? and channel_hash in (
        		select channel_hash from channels_names where name = ?)""",
        		(group_title, gr_name, channel_title))
        	conn.commit()
        except Exception as e:
            logger.error(repr(e))
        conn.close()

    def get_groups(self):
        conn = sqlite3.connect(DB)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        groups = conn.cursor().execute("""
            select (select count(*) from channels_groups) as cnt,
            -1 as disabled, 'ВСЕ КАНАЛЫ' as group_title
            union all
            select * from (
            select count(cg.channel_hash) as cnt, g.disabled,
            g.title as group_title
            from groups g
            left join channels_groups cg on g.title = cg.group_title
            group by g.title order by g.title)
            """).fetchall()
        return groups
        conn.close()

    def group_toggle(self, name, status):
        conn = sqlite3.connect(DB)
        try:
            conn.cursor().execute("""
                update groups set disabled = ?
                where title = ?""",
                (int(not status), name))
            conn.commit()
        except: pass
        conn.close()

    def link_toggle(self, hash_, status):
        conn = sqlite3.connect(DB)
        try:
            conn.cursor().execute("""
                update channels_orig set disabled = ?
                where hash = ?""",
                (int(not status), hash_))
            conn.commit()
        except Exception as e: logger.error(repr(e))
        conn.close()

    def get_channels(self, name=None, disabled=False, group=None):
        conn = sqlite3.connect(DB)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        channels = []
        if name:
            channels_db = conn.cursor().execute("""
                select co.*, cn.name from channels_orig co
                inner join channels_names cn on co.hash = cn.channel_hash
                inner join resources r on co.resource = r.resource and r.disabled = 0
                where cn.name = '{0}'
                order by cn.name, cost
                """.format(name.encode('utf8').replace("'","''"))).fetchall()
        elif disabled:
            group_filter = ""
            if group: group_filter = "where group_title = '{}'".format(group.encode('utf8'))
            channels_db = conn.cursor().execute("""
                select * from channels {}
                """.format(group_filter)).fetchall()
        else:
            channels_db = conn.cursor().execute("""
                select * from channels
                where gr_disabled = 0
                and ch_disabled <> cnt
                """).fetchall()
        channels = channels_db
        conn.close()
        return channels

    def get_channel(self, name, hd_priority=0, p2p_priority=0,
                          acestream_host=addon.getSetting('ace_host'), acestream_port=addon.getSetting('ace_port')):
        channels = self.get_channels(name)
        addon = xbmcaddon.Addon()
        if channels:
            channels = self.order_channels(channels, hd_priority=hd_priority, p2p_priority=p2p_priority)
            for channel in channels:
                logger.debug('%s == %s', channel['resource'], addon.getSetting(channel['resource']))
                if addon.getSetting(channel['resource']) == 'false': continue
                if channel['disabled'] == 1: continue
                module = 'modules.'+channel['resource'][:-3]
                url = importlib.import_module(module).TVResource().get_stream(channel)
                if url:
                    if url.startswith('/ace/'):
                        url = ''.join(['http://', acestream_host, ':', acestream_port, url])
                    logger.info('get_stream: %s', url)
                    test = self.test_channel(url, acestream_host, acestream_port)
                    logger.info('test %s: %s', url, test)
                    if test < 999: return url
            logger.error('%s: no working streams', name)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'),
                '%s: нет рабочих потоков' % (name.encode('utf8')), 1000, ''))

    def channel_toggle(self, name, status):
        conn = sqlite3.connect(DB)
        try:
            conn.cursor().execute("""
                update channels_orig set disabled = ?, timestamp = ?
                where hash in (select channel_hash from channels_names where name = ?)""",
                (int(not status), int(time.time()-time.mktime(time.gmtime(0))), name))
            conn.commit()
        except: pass
        conn.close()

    def get_playlist(self, hd_priority=0, p2p_priority=0,
                           acestream_host=addon.getSetting('ace_host'), acestream_port=addon.getSetting('ace_port')):
        m3u = []
        m3u.append('#EXTM3U')
        for channel in self.get_channels():
            logo = self.get_logo(channel)
            m3u.append(''.join([
                '#EXTINF:-1 group-title="', channel.get('group_title'),
                '" tvg-name="', channel.get('name'),
                '" tvg-id="" tvg-logo="', logo,
                '",', channel.get('name')
            ]))
            url = [
                'http://{host}:{port}/channel?name={name}&hd={hd}&p2p={p2p}'.format(
                    host=addon.getSetting('host'),
                    port=addon.getSetting('port'),
                    name=urllib2.quote(channel.get('name').encode('utf8')),
                    hd=hd_priority,
                    p2p=p2p_priority
                )]
            if acestream_host != addon.getSetting('ace_host'): url.append('acestream_host='+acestream_host)
            if acestream_port != addon.getSetting('ace_port'): url.append('acestream_port='+acestream_port)
            m3u.append('&'.join(url))
        return '\n'.join(m3u)

    def order_channels(self, channels, hd_priority=0, p2p_priority=0):
        tmp = channels
        result = []
        if hd_priority:
            result.extend([c for c in tmp if re.search('HD', c['title'])])
            result.extend([c for c in tmp if not re.search('HD', c['title'])])
        else:
            result.extend([c for c in tmp if not re.search('HD', c['title'])])
            result.extend([c for c in tmp if re.search('HD', c['title'])])
        tmp = result
        result = []
        if p2p_priority:
            result.extend([c for c in tmp if re.search('(^/ace/|acestream)', c['link'])])
            result.extend([c for c in tmp if not re.search('(^/ace/|acestream)', c['link'])])
        else:
            result.extend([c for c in tmp if not re.search('(^/ace/|acestream)', c['link'])])
            result.extend([c for c in tmp if re.search('(^/ace/|acestream)', c['link'])])
        return result

    def test_channel(self, url, acestream_host, acestream_port):
        try:
            s = requests.session()
            d = datetime.now()
            if '/ace/' in url:
                url = url.replace('ace/getstream', 'ace/manifest.m3u8')
                link = ''.join([
                    'http://', acestream_host, ':', acestream_port,
                    '/webui/api/service?method=get_version&format=jsonp&callback=mycallback'
                ])
                result = self._request(link)
                if result:
                    return 1.
                else:
                    return 999.
            else:
                try:
                    r = s.get(url, timeout=(1, 0.00001))
                except requests.exceptions.ReadTimeout:
                    delta = datetime.now()-d
                    return float(delta.microseconds)/1000
                except requests.exceptions.ConnectTimeout:
                    logger.error('error test channel %s: ConnectTimeout', url)
                    return 999.
        except Exception as e:
            logger.error('error test channel %s: %s', url, repr(e))
            return 999.

    def get_logo(self, channel):
        try:
            m = [f.encode('utf8') for f in os.listdir(os.path.join(GLOBAL_PATH,'static','images','logos'))]
            f = m[m.index(channel['name']+'.png')]
            return 'http://{host}:{port}/static/images/logos/{name}'.format(
                host=addon.getSetting('host'),
                port=addon.getSetting('port'),
                name=urllib2.quote(f)
            )
        except:
            if channel['logo']: return channel['logo']
            else: return ''
