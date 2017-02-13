#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 18:50:47 2017

@author: clesiemo3
"""

import feedparser
import facebook
import config
import html
import re
import sheets
from datetime import datetime as dt

# efree
feed = feedparser.parse('http://www.efree.org/events/feed/')

message = "Weekly Announcements\nPosted by Bot - Report issues in comments\n"

message += sheets.yalt_schedule()

for x in feed.entries:
    message += "\n" + x.title
    message += "\n" + x.link
    message += "\n" + dt.strptime(x.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%A %B %d %H:%M %p')
    summary = re.sub(r' <a href.+more.+$', '... [truncated]', x.summary)
    message += "\n" + summary + "\n"

message = html.unescape(message)

# facebook
graph = facebook.GraphAPI(config.user_token)
groups = graph.get_object("me/groups")

group_id = [x for x in groups['data'] if x['name'] == "yalt-test"][0]['id']
graph.put_wall_post(message = message, profile_id = group_id)

print(message)

