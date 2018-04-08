#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 18:50:47 2017

@author: clesiemo3
"""

import feedparser
import html2text
import requests
import html
import re
import sheets
import os
import datetime as dttm
from datetime import datetime as dt
import sendgrid
from sendgrid.helpers.mail import *

# py files
import auth_flow


def main():
    sep = "##############################################"
    message = "Weekly Announcements<br>Posted by Bot - Report issues in comments<br>"

    message += sheets.ya_schedule() + "<br>"

    try:
        sermon = feedparser.parse("http://www.efree.org/sermons/feed/").entries[0]
        vimeo_link = re.findall(r"https://player.vimeo.com/video/[0-9]+", sermon['content'][0]['value'])[0]
        sermon_string = "Last Week's Sermon - {0} - {1} <br>Link: {2} <br>Vimeo: {3} <br>MP3 download: {4} <br>"
        message += sermon_string.format(sermon.title, sermon.author, sermon.link, vimeo_link, sermon.links[1]['href'])
        # message += "<br>{sep}<br>{sep}<br>".format(sep=sep)
    except Exception as e:
        print(e)
        pass

    # facebook
    group_id = os.environ['fb_group_id']
    now = dt.now()
    buffer = dttm.timedelta(days=31)
    until = now + buffer
    efree_mask = '%Y-%m-%d %H:%M:%S'
    output_mask = '%A %B %d %I:%M %p'

    message += "<br>Efree Events<br>" + sep + "<br>" + sep + "<br>"
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
        msg_x = "<br>" + x.get("title", "Event Name")
        msg_x += "<br>" + x.get("url", "")
        start_date = dt.strptime(x.get("start_date", now), efree_mask)
        if x.get("all_day", False):
            msg_x += "<br>" + start_date.strftime("%A %B %d")
        else:
            msg_x += "<br>" + start_date.strftime(output_mask)
        # summary = re.sub(r' <a href.+more.+$', '... [truncated]', x.summary)
        msg_x += h.handle(x.get("description", ""))
        msg_x += "<br>" + sep + "<br>"

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
        # using SendGrid's Python Library
        # https://github.com/sendgrid/sendgrid-python
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("young.adults@efree.org")
        to_email = Email(os.environ['send_email'])
        subject = "Young Adults News - {0}".format(now.date().isoformat())
        content = Content("text/html", message)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
