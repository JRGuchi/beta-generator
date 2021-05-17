import requests

# Basic constant(s)
base_url = 'https://data.messari.io'

# All requests to Messari API can be made through this class
# API documentation found here: https://messari.io/api/docs
class Messari:

    def __init__(self, key=None):
        '''
        Initialize the object with the API key.
        '''
        print('Messari API session initialized.')
        self.key = key
        self.session = requests.Session()
        if self.key:
            self.session.headers.update({'x-messari-api-key': key})
            print('Key confirmed.' + '\n')
        else:
            print('No key provided.' + '\n')

    def _send_message(self, method, endpoint, params=None, data=None):
        '''
        Send the API request. Messari only offers GET endpoints at this time.
        
        - method: GET, POST, etc.
        - endpoint: append to base URL
        - params: HTTP request params
        - data: JSON payload for POST
        '''
        url = base_url + endpoint
        r = self.session.request(method, url, params=params, data=data, timeout=10)
        '''
        Uncomment the below if troubleshooting:
        print("URL: ", url)
        print("Params: ", params)
        print("Data: ", data)
        '''
        return r.json()

    def _get(self, endpoint, params=None):
        '''
        Messari only offers GET endpoints at this time, so 'GET' is automatically specified.
        
        - endpoint: append to base URL with working version
        - params: HTTP request params
        '''
        return self._send_message('GET', endpoint, params=params)

    def get_all_assets(self, **query_params):
        '''
        Get the paginated list of all assets and their metrics and profiles.
        Can optionally use ?fields, ?with-metrics, and/or ?with-profiles to pare down the returned fields.

        Endpoint: GET /api/v2/assets
        
        - query_params: (dict) Dictionary of query parameters to filter the list
        '''
        path = '/api/v2/assets'
        
        if query_params.get('with-profiles', False) and query_params.get('with-metrics', False):
            path += '?with-metrics&with-profiles'
        elif query_params.get('with-profiles', False):
            path += '?with-profiles'
        elif query_params.get('with-metrics', False):
            path += '?with-metrics'

        if 'with-metrics' in query_params:
            del query_params['with-metrics']
        if 'with-profiles' in query_params:
            del query_params['with-profiles']

        return self._get(path, params=query_params)

    def get_asset(self, asset_key, fields=None):
        '''
        Get basic metadata for an asset.
        
        Endpoint: GET /api/v1/assets/{assetKey}
        
        - asset_key: (str) Can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        - fields: (str) Pare down the returned fields (comma , separated, drill down with a slash /)
        '''
        path = f'/api/v1/assets/{asset_key}'
        param = {
            'fields': fields
        }

        return self._get(path, params=param)

    def get_asset_profile(self, asset_key, fields=None):
        '''
        Get qualitative information for an asset.
        
        Endpoint: GET /api/v2/assets/{assetKey}/profile
        
        - asset_key: (str) Can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        - fields: (str) Pare down the returned fields (comma , separated, drill down with a slash /)
            - example: fields='id,slug,symbol,metrics/market_data/price_usd'
        '''
        path = f'/api/v2/assets/{asset_key}/profile'
        param = {
            'fields': fields
        }

        return self._get(path, params=param)

    def get_asset_metrics(self, asset_key, fields=None):
        '''
        Get quantitative information for an asset.
        
        Endpoint: GET /api/v1/assets/{assetKey}/metrics
        
        - asset_key: (str) Can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        - fields: (str) Pare down the returned fields (comma , separated, drill down with a slash /)
            - example: fields='id,slug,symbol,metrics/market_data/price_usd'
        '''
        path = f'api/v1/assets/{asset_key}/metrics'
        param = {
            'fields': fields
        }

        return self._get(path, params=param)

    def get_asset_market_data(self, asset_key, fields=None):
        '''
        Get the latest market data for an asset. This data is also included in the metrics endpoint, but if all you need is market data, use this.
        
        Endpoint: GET /api/v1/assets/{assetKey}/metrics/market-data
        
        - asset_key: (str) Can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        - fields: (str) Pare down the returned fields (comma , separated, drill down with a slash /)
            - example: fields='id,slug,symbol,metrics/market_data/price_usd'
        '''
        path = f'api/v1/assets/{asset_key}/metrics/market-data'
        param = {
            'fields': fields
        }

        return self._get(path, params=param)

    def list_asset_timeseries_metric_ids(self):
        '''
        Lists all of the available timeseries metric IDs for assets.
        
        Endpoint: GET /api/v1/assets/metrics
        '''
        path = f'/api/v1/assets/metrics'
        return self._get(path)

    def get_asset_timeseries(self, asset_key, metric_id, **query_params):
        '''
        Retrieve historical timeseries data for an asset.
        The list of supported metric IDs can be found at https://data.messari.io/api/v1/assets/metrics
        You can specify the timeframe in your parameters using (begin, end, start, before, after) query parameters. All range parameters are inclusive of the specified date. Supported intervals are ["5m", "15m", "30m", "1h", "1d", "1w"]. For any given interval, at most 2016 points will be returned.

        Endpoint: GET /api/v1/assets/{assetKey}/metrics/{metricID}/time-series

        - asset_key: (str) Can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        - metric_id: (str) Specifies which timeseries will be returned
        - query_params: (dict) Dictionary of query parameters to filter the list
        '''
        path = f'/api/v1/assets/{asset_key}/metrics/{metric_id}/time-series'
        return self._get(path, params=query_params)

    def get_all_markets(self, fields=None):
        '''
        Get the list of all exchanges and pairs that Messari's WebSocket-based market real-time market data API supports.

        Endpoint: GET /api/v1/markets

        - fields: (str) Pare down the returned fields (comma , separated, drill down with a slash /)
            - example: fields='id,slug,symbol,metrics/market_data/price_usd'
        '''
        path = f'/api/v1/markets'
        param = {
            'fields': fields
        }
        
        return self._get(path, params=param)

    def get_market_timeseries(self, market_key, metric_id, **query_params):
        '''
        Retrieve historical timeseries data for a market.

        Endpoint: GET /api/v1/markets/{marketKey}/metrics/{metricID}/time-series

        - market_key: (str) Can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        - metric_id: (str) Specifies which timeseries will be returned
        - query_params: (dict) Dictionary of query parameters to filter the list
        '''
        params = []
        for key,value in query_params.items():
            params.append(f'{key}={value}')

        params = '&'.join(params)
        
        path = f'api/v1/markets/{market_key}/metrics/{metric_id}/time-series'
        return self._get(path, params=query_params)

    def get_all_news(self, page=None, fields=None):
        '''
        Get the latest (paginated) news and analysis for all assets.

        Endpoint: GET /api/v1/news

        - page: (int) Page number, starts at 1. Increment to paginate through results (until result is empty array)
        - fields: (str) Pare down the returned fields (comma , separated, drill down with a slash /)
            - example: fields='id,slug,symbol,metrics/market_data/price_usd'
        '''
        path = '/api/v1/news'
        param = {
            'fields': fields
        }
        
        if page:
            param['page'] = page

        return self._get(path, params=param)

    def get_news_for_asset(self, asset_key, page=None, fields=None):
        '''
        Get the latest (paginated) news and analysis for an asset.

        Endpoint: GET /api/v1/news/{assetKey}

        - asset_key: (str) Can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        - page: (int) Page number, starts at 1. Increment to paginate through results (until result is empty array)
        - fields: (str) Pare down the returned fields (comma , separated, drill down with a slash /)
            - example: fields='id,slug,symbol,metrics/market_data/price_usd'
        '''
        path = f'/api/v1/news/{asset_key}'
        param = {
            'fields': fields
        }
        if page:
            param['page'] = page

        return self._get(path, params=param)