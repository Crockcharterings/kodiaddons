#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, logging, json, urllib2, sqlite3
logging.basicConfig(level = 'INFO')
logger = logging.getLogger(__name__)

#from channels import Channels
#chls = Channels()
#chls.update_channels()

from modules.allfontv import TVResource
res = TVResource()
res.get_channels()
print res.get_stream({'link':u' http://allfon-tv.com/?id=72#1'})
