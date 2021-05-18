import os
import pickle
import yaml

from APIs.messari_api import Messari

# Load secrets
with open('no-nos.yaml', 'rb') as f:
    uhoh = yaml.load(f, Loader=yaml.FullLoader)

messari_api_key = uhoh['messari_api_key']

# Begin session
messari = Messari(messari_api_key)

# Load tickers
with open('ticker_list.pickle', 'rb') as f:
    ticker_list = pickle.load(f)

# Uncomment the below for a refresher on available time series metric IDs
'''
metric_ids = messari.list_asset_timeseries_metric_ids()
for data in metric_ids['data']['metrics']:
    pprint.pprint(data)
'''

# Set parameters for the metrics you want time series of. For now, we are just doing price
# Future: 'sply.addr.bal.10k', 'exch.flow.in.ntv', 'exch.flow.in.usd', 'txn.tfr.erc721.cnt', 'addr.bal.10.ntv.cnt', 'txn.fee.avg', 'txn.cnt', 'hash.rev', 'mcap.out', 'txn.tsfr.val.avg', etc.
metric_id_list = ['price']
with open('metric_id_list.pickle', 'wb') as f: # We will unpickle and reference these metrics throughout
    pickle.dump(metric_id_list, f)

# Loop through our list of metric IDs and create directories for each
def create_metric_directories():
    
    if not os.path.exists('time_series_dfs'):
        os.makedirs('time_series_dfs')

    for metric in metric_id_list:
        if not os.path.exists(f'time_series_dfs/{metric}.csv'):
            os.makedirs(f'time_series_dfs/{metric}.csv')
        else:
            pass

create_metric_directories()