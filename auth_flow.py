#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 20:33:26 2017

@author: clesiemo3
"""

import requests
import json
import config

# initial token getter
# https://www.facebook.com/v2.8/dialog/oauth?client_id=1642664639360405&redirect_uri=http://localhost&response_type=token&scope=user_managed_groups,publish_actions,user_events

def get_new_token(old_token):
    url = "https://graph.facebook.com/v2.8/oauth/access_token?"
    params = {"grant_type":"fb_exchange_token",
              "client_id": config.client_id,
              "client_secret": config.client_secret,
              "fb_exchange_token": old_token}

    r = requests.get(url, params)
    token = json.loads(r.text)["access_token"]
    return(token)

# refresh token
def update_token():
    with open('user_token.json', 'r') as ut_file:    
        ut = json.load(ut_file)
    
    new_token = get_new_token(ut['user_token'])
    ut['user_token'] = new_token
    
    with open('user_token.json', 'w') as ut_file:    
        json.dump(ut, ut_file)
    
    return(new_token)
