import os, sys, webbrowser, fitbit

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
    
    verifier = input('Please input PIN: ')

    # get access token
    print('\n* Obtain an access token ...\n')
    token = client.fetch_access_token(verifier)

    global user_id, user_key, user_secret

    user_key = token['oauth_token']
    user_secret = token['oauth_token_secret']

    print('* Your user key is %s and your user secret is %s. These will be saved in config.txt.' % (user_key, user_secret))
    
    # lets create that config file for next time...
    cfgfile = open("./config.cfg",'w')

    # add the settings to the structure of the file, and lets write it out...
    config.add_section('Passkey')
    config.set('Passkey','user_key', user_key)
    config.set('Passkey','user_secret', user_secret)
    config.write(cfgfile)
    cfgfile.close()
    
def gather_data(auth, path, activity_type):
    t = auth.time_series('%s/%s' % (path, activity_type), period='1m')
    print(t['%s-%s' % (path, activity_type)][-1]['value'])
    

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
    elif (len(sys.argv) > 2):
        print("Please only use 1 argument at a time to make it compatible with Conky.")
        sys.exit(1)
    user_input = sys.argv[1]
    
    if user_input in ('-h', '--help'):
        print('''--help\tor -h\t to display this helpfile.
        ''')
    if user_input == '-s' or user_input == '--steps':
        gather_data(authd_client, 'activities', 'steps')

    #gather_data('activities', 'steps')
    gather_data(authd_client, 'sleep', 'minutesAsleep')
    gather_data(authd_client, 'activities', 'floors')
    gather_data(authd_client, 'activities', 'distance')
    gather_data(authd_client, 'activities', 'calories')
    gather_data(authd_client, 'activities', 'minutesSedentary')
    #print('\n')
    #gather_data('minutesLightlyActive')
    #gather_data('minutesFairlyActive')
    #gather_data('minutesVeryActive')
