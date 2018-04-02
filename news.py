#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 18:50:47 2017

@author: clesiemo3
"""

import feedparser
import html2text
import requests
import facebook
import html
import re
import sheets
import os
import datetime as dttm
from datetime import datetime as dt

# py files
import auth_flow


def main():
    sep = "##############################################"

    graph = facebook.GraphAPI(auth_flow.update_token())

    message = "Weekly Announcements\nPosted by Bot - Report issues in comments\n"

    message += sheets.ya_schedule() + "\n"

    sermon = feedparser.parse("http://www.efree.org/sermons/feed/").entries[0]
    vimeo_link = re.findall(r"https://player.vimeo.com/video/[0-9]+", sermon['content'][0]['value'])[0]
    sermon_string = "Last Week's Sermon - {0} - {1}\nLink: {2}\nVimeo: {3}\nmp3 download: {4}\n"
    message += sermon_string.format(sermon.title, sermon.author, sermon.link, vimeo_link, sermon.links[1]['href'])
    message += "\n{sep}\n{sep}\n".format(sep=sep)

    # facebook
    group_id = os.environ['fb_group_id']
    now = dt.now()
    buffer = dttm.timedelta(days=31)
    until = now + buffer
    events = graph.get_object(group_id + "/events",
                              since=now.strftime('%Y-%m-%d'),
                              until=until.strftime('%Y-%m-%d'))
    url_stub = "https://www.facebook.com/events/"
    fb_mask = '%Y-%m-%dT%H:%M:%S%z'
    efree_mask = '%Y-%m-%d %H:%M:%S'
    output_mask = '%A %B %d %I:%M %p'

    if events['data']:
        message += "\nYoung Adults Events\n"
        try:
            for event in events['data']:
                message += "\n" + event['name']
                message += "\n" + url_stub + event['id'] + "/"
                message += "\n" + dt.strptime(event['start_time'], fb_mask).strftime(output_mask)
                try:
                    message += " to " + dt.strptime(event['end_time'], fb_mask).strftime('%H:%M %p')
                except KeyError:
                    pass
                message += "\nLocation: " + event['place']['name']
                message += "\n\n" + event['description']
                message += "\n" + sep + "\n"
        except Exception as e:
            print(e)
    else:
        message += "\nNo Young Adult Facebook Events in the next 4 weeks\n"

    message += "\n\nEfree Events\n" + sep +"\n" + sep + "\n"
    exclude = re.compile("(Junior High Spring Retreat|Senior High|KampOut)")

    # efree

    efree_events = "http://www.efree.org/wp-json/tribe/events/v1/events"
    query_params = {"start_date": now.strftime(efree_mask),  # "2018-04-01 00:00:00",
                    "end_date": until.strftime(efree_mask),  # "2018-05-01 00:00:00",
                    "status": "publish"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

    events = requests.get(efree_events, params=query_params, headers=headers)
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_emphasis = True

    for x in events.json()['events']:
        print(x)
        msg_x = "\n" + x.get("title", "Event Name")
        msg_x += "\n" + x.get("url", "")
        start_date = dt.strptime(x.get("start_date", now), efree_mask)
        if x.get("all_day", False):
            msg_x += "\n" + start_date.strftime("%A %B %d")
        else:
            msg_x += "\n" + start_date.strftime(output_mask)
        # summary = re.sub(r' <a href.+more.+$', '... [truncated]', x.summary)
        msg_x += h.handle(x.get("description", ""))
        msg_x += sep + "\n"

        if exclude.search(msg_x):
            print("Excluded!")
            print(msg_x)
            continue
        else:
            message += msg_x

    message = html.unescape(message)

    if eval(os.environ['print_only']):
        print(message)
    else:
        graph.put_wall_post(message=message, profile_id=group_id)
