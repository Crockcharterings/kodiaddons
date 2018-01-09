# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui
import os, sys, json, logging

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
sys.path.insert(0, os.path.join(addon.getAddonInfo('path'),'resources','lib'))

from flask import (Flask, render_template, Response, redirect, url_for, request, jsonify, abort)
from channels import Channels

logging.basicConfig(
    format     = addon.getSetting('log_format'),
    level      = addon.getSetting('log_level'),
    filename   = os.path.join(addon.getAddonInfo('path'), 'addon.log')
)
logger = logging.getLogger(__name__)
app = Flask(__name__)
chls = Channels()

def jsonloads(value):
    try: return json.loads(value)
    except: return value

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/groups/get')
def api_groups_get():
    groups = chls.get_groups()
    return jsonify(groups=dict(get=groups))

@app.route('/api/groups/disable')
def api_groups_disable():
    name = request.args.get('name')
    status = jsonloads(request.args.get('status'))
    if name and isinstance(status, bool):
        chls.group_toggle(name, status)
        return jsonify(groups=dict(disable=dict(
            name=name, status=status)))
    return abort(400)

@app.route('/api/channels/get')
def api_channels_get():
    group = request.args.get('group')
    channels = chls.get_channels(disabled=True, group=group)
    return jsonify(channels=dict(get=channels))

@app.route('/api/channels/links')
def api_channels_links():
    name = request.args.get('name')
    if name:
        channels = chls.get_channels(name)
        return jsonify(channels=dict(links=channels))
    return abort(400)

@app.route('/api/channels/disable')
def api_channels_disable():
    name = request.args.get('name')
    status = jsonloads(request.args.get('status'))
    if name and isinstance(status, bool):
        chls.channel_toggle(name, status)
        return jsonify(channels=dict(disable=dict(
            name=name, status=status)))
    return abort(400)

@app.route('/api/channels/disable_resource')
def api_channels_disable_resource():
    hash_ = request.args.get('hash')
    status = jsonloads(request.args.get('status'))
    if hash_ and isinstance(status, bool):
        chls.link_toggle(hash_, status)
        return jsonify(channels=dict(disable_resourse=dict(
            hash=hash_, status=status)))
    return abort(400)

@app.route('/api/channels/update')
def api_channels_update():
    ch_name = request.args.get('ch_name')
    gr_name = request.args.get('gr_name')
    channel_title = request.args.get('channel_title')
    group_title = request.args.get('group_title')
    if len(channel_title) > 0:
        chls.update_channel(ch_name, gr_name, channel_title, group_title)
        return jsonify(channels=dict(update=dict(
            ch_name=ch_name, gr_name=gr_name,
            channel_title=channel_title, group_title=group_title)))
    return abort(400)

@app.route('/playlist')
def playlist():
    ace_host = request.args.get('ace_host',addon.getSetting('ace_host'))
    ace_port = request.args.get('ace_port',addon.getSetting('ace_port'))
    hd = request.args.get('hd',int(jsonloads(addon.getSetting('hd'))))
    p2p = request.args.get('p2p',int(jsonloads(addon.getSetting('p2p'))))
    m3u = chls.get_playlist(
        hd=hd, p2p=p2p,
        ace_host=ace_host, ace_port=ace_port)
    return Response(m3u, status=200, mimetype='text/plain')

@app.route('/channel')
def channel():
    name = request.args.get('name')
    ace_host = request.args.get('ace_host',addon.getSetting('ace_host'))
    ace_port = request.args.get('ace_port',addon.getSetting('ace_port'))
    hd = request.args.get('hd',int(jsonloads(addon.getSetting('hd'))))
    p2p = request.args.get('p2p',int(jsonloads(addon.getSetting('p2p'))))
    channel_link = chls.get_channel(name,
        hd=hd, p2p=p2p,
        ace_host=ace_host, ace_port=ace_port)
    if channel_link: return redirect(channel_link)
    return abort(403)

if __name__ == '__main__':
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addonname, 'запустился', 5000, ''))
    app.run(host='0.0.0.0', debug=False, threaded=True, port=int(addon.getSetting('port')))
