import pickle
import pprint
import yaml

from APIs.messari_api import Messari

# Load secrets
with open('no-nos.yaml', 'rb') as f:
    uhoh = yaml.load(f, Loader=yaml.FullLoader)

messari_api_key = uhoh['messari_api_key']

# Begin session
messari = Messari(messari_api_key)

# Pull asset tickers you are interested in
ticker_list = []
def get_all_assets():    
    pages = 2  # Only grabbing the top 40 assets for now to avoid future rate limiting
    for i in range(pages):
        query_params = {
            'page': i+1,
            '?fields': 'symbol'
        }
        assets_dict = messari.get_all_assets(**query_params)
        for asset in assets_dict['data']:
            if (asset['symbol'] == 'BTT' or asset['symbol'] == 'COIN'): # We are omitting these symbols as they are not returning full time series
                pass
            else:
                ticker_list.append(asset['symbol'])

    with open('ticker_list.pickle', 'wb') as f: # We will unpickle and reference these tickers throughout
        pickle.dump(ticker_list, f)

    print(ticker_list)
    print('Ticker count: ' + str(len(ticker_list)))

get_all_assets()