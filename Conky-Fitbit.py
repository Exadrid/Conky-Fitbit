#!/usr/bin/python

from fitbit.api import FitbitOauthClient

import os, sys, webbrowser, fitbit, time, datetime

import configparser
config = configparser.ConfigParser()

client_key = 'ba7c8a6d4376449f8ed481f0af25c7e2'
client_secret = '69f323833a91491cbac4fdc4ff219bdc'

def gather_keys():
    
    print('* Obtain a request token ...\n')
    client = FitbitOauthClient(client_key, client_secret)
    token = client.fetch_request_token()
    
    stderr = os.dup(2)
    os.close(2)
    os.open(os.devnull, os.O_RDWR)
    try:
        webbrowser.get().open(client.authorize_token_url())
    finally:
        os.dup2(stderr, 2)
        
    print('* Authorize the request token in your browser\n')
    time.sleep(3)
    
    verifier = input('\nPlease input PIN: ')
        
    # get access token
    print('\n* Obtain an access token ...\n')
    token = client.fetch_access_token(verifier)

    global user_id, user_key, user_secret

    user_key = token['oauth_token']
    user_secret = token['oauth_token_secret']

    print('* Your user key is %s and your user secret is %s. These will be saved in config.cfg.' % (user_key, user_secret))
    
    # lets create that config file for next time...
    cfgfile = open("./config.cfg",'w')

    # add the settings to the structure of the file, and lets write it out...
    config.add_section('Passkey')
    config.set('Passkey','user_key', user_key)
    config.set('Passkey','user_secret', user_secret)
    config.write(cfgfile)
    cfgfile.close()

def gather_data(auth, path, activity_type, time_input):
    if time_input == '1d':
        date_list = (auth.time_series('%s/%s' % (path, activity_type), period=time_input))
        final_sum = next (iter (date_list.values()))[-1]['value']
    elif time_input in('1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y'):
        date_list = (auth.time_series('%s/%s' % (path, activity_type), period=time_input))
        final_sum = 0
        for item in range(len(next (iter (date_list.values())))):
            final_sum = final_sum + int(next (iter (date_list.values()))[item]['value'])
    elif time_input == 'yesterday':
        date_list = (auth.time_series('%s/%s' % (path, activity_type), period='1w'))
        final_sum = next (iter (date_list.values()))[-2]['value']
    elif len(time_input) == 10:
        date_list = (auth.time_series('%s/%s' % (path, activity_type), period='max'))
        date = next (iter (date_list.values()))
        for item in range(len(date)):
            if (date[item]['dateTime']) == time_input:
                final_sum = (date[item]['value'])
    elif time_input == 'last_week':
        date_list = (auth.time_series('%s/%s' % (path, activity_type), period='max'))
        date_list2 = next (iter (date_list.values()))
        date_list3 = date_list2[-days_since_sunday:]
        final_sum = 0
        for item in range(len(date_list3)):
            final_sum = final_sum + int(date_list3[item]['value'])
    return(final_sum)





if not os.path.exists("/home/eric/.conky/Fitbit/config.cfg"):
    gather_keys()

config.read('/home/eric/.conky/Fitbit/config.cfg')
user_key = config.get('Passkey', 'user_key')
user_secret = config.get('Passkey', 'user_secret')

authd_client = fitbit.Fitbit(client_key, client_secret, resource_owner_key=user_key, resource_owner_secret=user_secret)
    

#days since last sunday
d = datetime.datetime.today()
today = datetime.date(d.year, d.month, d.day)
days_since_sunday = today.weekday() + 1

steps_today = gather_data(authd_client, 'activities', 'steps', "1d")
today_ff = open('/home/eric/.conky/Fitbit/steps_format.txt', 'w')
today_ff.write(steps_today)
if int(steps_today) > 10000:
    steps_today = 10000
    today_f = open('/home/eric/.conky/Fitbit/steps.txt', 'w')
    today_f.write(str(steps_today))
else:
    today_f = open('/home/eric/.conky/Fitbit/steps.txt', 'w')
    today_f.write(str(steps_today))

steps_this_week = gather_data(authd_client, 'activities', 'steps', "last_week")
week_ff = open('/home/eric/.conky/Fitbit/week_format.txt', 'w')
week_ff.write(str(steps_this_week))
if int(steps_this_week) > 70000:
    steps_this_week = 70000
    week_f = open('/home/eric/.conky/Fitbit/week.txt', 'w')
    week_f.write(str(steps_this_week))
else:
    week_f = open('/home/eric/.conky/Fitbit/week.txt', 'w')
    week_f.write(str(steps_this_week))

daily_floors = gather_data(authd_client, 'activities', 'floors', "1d")
floor_ff = open('/home/eric/.conky/Fitbit/floor_format.txt', 'w')
floor_ff.write(str(daily_floors))
