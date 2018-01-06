# -*- coding: utf-8 -*-

import xbmcaddon
import xbmcgui
import sys
import os

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

sys.path.insert(0, addon.getAddonInfo('path')+'/resources/lib/')

from flask import (Flask, render_template, Response, redirect, url_for, request, jsonify, abort)

#version = ".".join(map(str, sys.version_info[:3]))
#xbmcgui.Dialog().ok(addonname, addon.getAddonInfo('path'), __name__, version)

app = Flask(__name__)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True, port=8081)
