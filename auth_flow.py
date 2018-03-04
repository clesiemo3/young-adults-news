#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 20:33:26 2017

@author: clesiemo3
"""

import requests
import json
import os
import pygsheets

# initial token getter
# https://www.facebook.com/v2.8/dialog/oauth?client_id=1642664639360405&redirect_uri=http://localhost&response_type=token&scope=user_managed_groups,publish_actions,user_events


def get_new_token(old_token):
    url = "https://graph.facebook.com/%s/oauth/access_token?" % os.environ['fb_api_version']
    params = {"grant_type": "fb_exchange_token",
              "client_id": os.environ['fb_client_id'],
              "client_secret": os.environ['fb_client_secret'],
              "fb_exchange_token": old_token}

    r = requests.get(url, params)
    try:
        resp = json.loads(r.text)
        token = resp["access_token"]
        expires = resp["expires_in"]
        print("Token expires in {0} seconds ({1} days)".format(expires, round(expires/3600/24, 2)))
    except KeyError:
        print(resp)
        raise KeyError
    return token


# refresh token
def update_token():
    print('Refreshing token...')
    try:
        gc = pygsheets.authorize(service_file='client_secret.json')
    except FileNotFoundError:
        with open('client_secret.json', 'w') as cs_file:
            cs_file.write(os.environ['google_client_secret'])
        gc = pygsheets.authorize(service_file='client_secret.json')

    # because I'm not setting up an entire database for 1 token
    ws = gc.open_by_key(os.environ['token_sheets_id']).worksheet_by_title('token')
    new_token = get_new_token(ws.get_value('A2'))

    ws.update_cell('A2', new_token)
    
    return new_token
