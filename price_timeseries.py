import csv
import os
import pickle
import yaml

from datetime import date
from APIs.messari_api import Messari

# Load secrets
with open('no-nos.yaml', 'rb') as f:
    uhoh = yaml.load(f, Loader=yaml.FullLoader)

messari_api_key = uhoh['messari_api_key']

# Begin session
messari = Messari(messari_api_key)

# Load tickers and metrics
with open('ticker_list.pickle', 'rb') as f:
    ticker_list = pickle.load(f)

with open('metric_id_list.pickle', 'rb') as f:
    metric_id_list = pickle.load(f)

# Loop through our list of tickers and create directories for each ticker within each metric
def request_timeseries_price():
    
    if not os.path.exists('time_series_dfs'):
        return 'Check to ensure metric_dirs.py has run before calling this function.'
    else:
        pass
    
    query_params = {
        'start': '2021-01-01', # We will just use YTD time series for now
        'end': date.today(),
        'interval': '1d' # Anything under 1d requires an enterprise subscription
    }

    for metric in metric_id_list:
        if not os.path.exists(f'time_series_dfs/{metric}'):
            return f'{metric}: Check to ensure metric_dirs.py has run before calling this function.'
        else:
            metric_id = metric
            for ticker in ticker_list:
                if not os.path.exists(f'time_series_dfs/{metric}/{ticker}.csv'):
                    asset_key = ticker
                    metric_dict = messari.get_asset_timeseries(asset_key, metric_id, **query_params)

                    metric_data = metric_dict['data']
                    data_headers = metric_data['parameters']['columns']

                    with open(f'time_series_dfs/{metric}/{ticker}.csv', 'w') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(data_headers)
                        for row in metric_data['values']:
                            csv_writer.writerow(row)

request_timeseries_price()