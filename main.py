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
import datetime as dttm
from datetime import datetime as dt

# efree
feed = feedparser.parse('http://www.efree.org/events/feed/')

message = "Weekly Announcements\nPosted by Bot - Report issues in comments\n"

message += sheets.yalt_schedule()

# facebook
graph = facebook.GraphAPI(config.user_token)
groups = graph.get_object("me/groups")
group_id = [x for x in groups['data'] if x['name'] == "Young Adult's Ministry at First Free Church, Manchester, MO"][0]['id']
now = dt.now()
two_weeks = dttm.timedelta(days=14)
until = now + two_weeks
events = graph.get_object("195603127146892/events", 
                          since = now.strftime('%Y-%m-%d'), 
                          until = until.strftime('%Y-%m-%d'))
url_stub = "https://www.facebook.com/events/"
fb_mask = '%Y-%m-%dT%H:%M:%S%z'
efree_mask = '%a, %d %b %Y %H:%M:%S %z'
output_mask = '%A %B %d %I:%M %p'

message += "\nYoung Adults Events\n"
try:
    for event in events['data']:
        message += "\n" + event['name']
        message += "\n" + url_stub + event['id'] + "/"
        message += "\n" + dt.strptime(event['start_time'], fb_mask).strftime(output_mask) + \
                                     " to " + dt.strptime(event['end_time'], fb_mask).strftime('%H:%M %p')
        message += "\nLocation: " + event['place']['name']
        message += "\n\n" + event['description']
except Exception as e:
    message += "\n    No Young Adults Events in the next 2 weeks."
    print(e)

message += "\n\nEfree Events\n"
for x in feed.entries:
    message += "\n" + x.title
    message += "\n" + x.link
    message += "\n" + dt.strptime(x.published, efree_mask).strftime(output_mask)
    summary = re.sub(r' <a href.+more.+$', '... [truncated]', x.summary)
    message += "\n\n" + summary + "\n"

message = html.unescape(message)

graph.put_wall_post(message = message, profile_id = group_id)
print(message)

