#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 20:33:26 2017

@author: clesiemo3
"""

import requests
import config
import json

# https://www.facebook.com/v2.8/dialog/oauth?client_id=1642664639360405&redirect_uri=http://localhost&response_type=token&scope=user_managed_groups,publish_actions,user_events

url = "https://graph.facebook.com/v2.8/oauth/access_token?"
params = {"grant_type":"fb_exchange_token",
          "client_id": config.client_id,
          "client_secret": config.client_secret,
          "fb_exchange_token": config.user_token}

r = requests.get(url, params)
token = json.loads(r.text)["access_token"]
