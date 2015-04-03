import os
import sys
import pprint
import webbrowser
import fitbit

from fitbit.api import FitbitOauthClient

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

    user_id = token['encoded_user_id']
    user_key = token['oauth_token']
    user_secret = token['oauth_token_secret']

    print(user_id)
    print(user_key)
    print(user_secret)

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(token)
    #print('')


if __name__ == '__main__':

    #If it does not exist - TO DO
    gather_keys()
    
    #authd_client = fitbit.Fitbit(client_key, client_secret, resource_owner_key=user_key, resource_owner_secret=user_secret)
    #print(authd_client.activity_stats())
