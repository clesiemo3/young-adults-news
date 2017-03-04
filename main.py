#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 18:50:47 2017

@author: clesiemo3
"""

import feedparser
import facebook
import html
import re
import sheets
import datetime as dttm
from datetime import datetime as dt

# py files
import auth_flow

# efree
feed = feedparser.parse('http://www.efree.org/events/feed/')

message = "Weekly Announcements\nPosted by Bot - Report issues in comments\n"

message += sheets.yalt_schedule()

# facebook
graph = facebook.GraphAPI(auth_flow.update_token())
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

if events['data'] != []:
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
        print(e)
else:
    message += "\nNo Young Adult Facebook Events in the next 2 weeks\n"

message += "\n\nEfree Events\n"
exclude = re.compile("(Junior High|Senior High|KampOut)")
for x in feed.entries:
    msg_x = "\n" + x.title
    msg_x += "\n" + x.link
    msg_x += "\n" + dt.strptime(x.published, efree_mask).strftime(output_mask)
    summary = re.sub(r' <a href.+more.+$', '... [truncated]', x.summary)
    msg_x += "\n\n" + summary + "\n"
    if exclude.search(msg_x):
        print("Excluded!")
        print(msg_x)
        continue
    else:
        message += msg_x

message = html.unescape(message)

graph.put_wall_post(message = message, profile_id = group_id)
print(message)

