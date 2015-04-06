#!/usr/bin/env python
import os, sys, webbrowser, fitbit, time

from fitbit.api import FitbitOauthClient

import configparser
config = configparser.ConfigParser()

user_id = ''
user_key = ''
user_secret = ''
client_key = 'ba7c8a6d4376449f8ed481f0af25c7e2'
client_secret = '69f323833a91491cbac4fdc4ff219bdc'

def gather_keys():

    # setup
    print('** OAuth Python Library Example **\n')
    client = FitbitOauthClient(client_key, client_secret)

    # get request token
    print('* Obtain a request token ...\n')
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
    return(final_sum)


def print_funct(data_list):
    pass
    #print(data_list['%s-%s' % (path, activity_type)][-1]['value'])

if __name__ == '__main__':

    #If it does not exist - TO DO
    config_data = config.read('./config.cfg')
    if config_data == []:
        gather_keys()
    user_key = config['Passkey']['user_key']
    user_secret = config['Passkey']['user_secret']

    authd_client = fitbit.Fitbit(client_key, client_secret, resource_owner_key=user_key, resource_owner_secret=user_secret)

    if (len(sys.argv) < 2):
        print("Please add an argument. Use '--help' for helpfile.")
        sys.exit(1)
    elif (len(sys.argv) != 3) and not sys.argv[1] == '--help':
        print("Please use exactly 2 arguments. Use '--help' for helpfile.")
        sys.exit(1)
    
    activity_input = (sys.argv[1])
    
    if (len(sys.argv) == 3):
        time_input = (sys.argv[2])
        if time_input == '--today':
            time_input = '1d'
        else:
            time_input = time_input[2:]
        
    #Activity
    if activity_input in('--calories', '--caloriesBMR', '--steps', '--floors', '--elevation', '--minutesSedentary', '--minutesLightlyActive', '--minutesFairlyActive', '--minutesVeryActive', '--activityCalories'):
        data_list = gather_data(authd_client, 'activities', activity_input[2:], time_input)
        #print(data_list)
    #Sleep
    elif activity_input in('--startTime', '--timeInBed', '--minutesAsleep', '--awakeningsCount', '--minutesAwake', '--minutesToFallAsleep', '--minutesAfterWakeup', '--efficiency'):
        data_list = gather_data(authd_client, 'sleep', activity_input[2:], time_input)
        #print(data_list)
    #Body
    elif activity_input in('--weight', '--bmi', '--fat'):
        data_list = gather_data(authd_client, 'body', activity_input[2:], time_input)
        #print(data_list)
    elif activity_input in ('-h', '--help'):
        print('''\n--help to display this helpfile.
    
Example : "Conky-Steps.py --steps --1w"
Example : "Conky-Steps.py --efficiency --today"
Example : "Conky-Steps.py --floors --2015-03-26"

--------------------* Activities *--------------------

Time available = 'today', '7d', '30d', '1w', '1m', '3m', '6m', 
                 '1y', 'yesterday', or specify date ('YYYY-MM-DD')

--calories, --caloriesBMR, --steps, --floors, --elevation,
--minutesSedentary, --minutesLightlyActive, --minutesFairlyActive,
--minutesVeryActive, --activityCalories

--------------------* Sleep *--------------------

Time available = 'today', 'yesterday' or specify date ('YYYY-MM-DD')

--startTime, --timeInBed, --minutesAsleep, --awakeningsCount, 
--minutesAwake, --minutesToFallAsleep, --minutesAfterWakeup,
--efficiency

--------------------* Body *---------------------

Time available = 'today', 'yesterday' or specify date ('YYYY-MM-DD')

--weight, --bmi, --fat\n''')
        sys.exit(1)
    else:
        print('''Could not recognize the arguments. Here are some examples. --help for more.
        
Example : "Conky-Steps.py --steps --1w"
Example : "Conky-Steps.py --efficiency --today"
Example : "Conky-Steps.py --floors --2015-03-26"
''')
        sys.exit(1)
    print_funct(data_list)
    print(data_list)

