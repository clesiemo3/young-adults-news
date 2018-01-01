#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 20:11:05 2017

@author: clesiemo3
"""

import os
import pygsheets


def ya_schedule():
    message = '\n'
    error_message = '\nError: Failed to find schedule data from google sheets.\n'

    try:
        gc = pygsheets.authorize(service_file='client_secret.json')
    except FileNotFoundError:
        with open('client_secret.json', 'w') as cs_file:
            cs_file.write(os.environ['google_client_secret'])
            gc = pygsheets.authorize(service_file='client_secret.json')

    try:
        ws = gc.open_by_key(os.environ['sheets_id']).worksheet_by_title('Teaching Schedule')
        next_week = ws.get_values('A1', 'E2', include_all=True)
        # ugly dict comprehension to turn 1st list into keys
        nw_dict = {next_week[0][i]: next_week[1][i] for i in range(0, len(next_week[0]))}
        for k, v in nw_dict.items():
            if v == "":
                continue
            message += "%s: %s\n" % (k, v)
    except KeyError as e:
        print("KeyError: %s" % e)
        message = error_message
    except pygsheets.PyGsheetsException as e:
        print("PyGsheetsException: %s" % e)
        message = error_message
    
    return message
