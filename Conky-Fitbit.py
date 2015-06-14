from fitbit.api import FitbitOauthClient

import os, sys, webbrowser, fitbit, time

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


gather_keys()
