from datetime import date
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

# Uncomment the below for a refresher on available time series metric IDs
'''
metric_ids = messari.list_asset_timeseries_metric_ids()
for data in metric_ids['data']['metrics']:
    pprint.pprint(data)
'''

# Pull asset tickers you are interested in
ticker_list = []
def get_all_assets():    
    pages = 10  # I only care about the top 200 assets for now
    for i in range(pages):
        query_params = {
            'page': i+1,
            '?fields': 'symbol'
        }
        assets_dict = messari.get_all_assets(**query_params)
        for asset in assets_dict['data']:
            ticker_list.append(asset['symbol'])

    with open('ticker_list.pickle', 'wb') as f: # We will unpickle and reference these puppies later
        pickle.dump(ticker_list, f)

    print(ticker_list)
    print('Ticker count: ' + str(len(ticker_list)))

get_all_assets()