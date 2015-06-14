from fitbit.api import FitbitOauthClient



client_key = 'ba7c8a6d4376449f8ed481f0af25c7e2'
client_secret = '69f323833a91491cbac4fdc4ff219bdc'

def gather_keys():
    # setup
    print('** OAuth Python Library Example **\n')
    client = FitbitOauthClient(client_key, client_secret)
    
    print('* Obtain a request token ...\n')
    token = client.fetch_request_token()

gather_keys()
