import logging, requests
from utils import validate_basic_params

log = logging.getLogger()

SEARCH_ALL = 'all'
SEARCH_ASSETS = 'asset'
SEARCH_ALERTS = 'alert'
SEARCH_SIGNALS = 'signal'

_search_types = [ SEARCH_ALL, SEARCH_ASSETS, SEARCH_ALERTS, SEARCH_SIGNALS, ]

_search_uris = {
    SEARCH_ALL : '/api/search',
    SEARCH_ASSETS: '/api/search/assets',
    SEARCH_ALERTS: '/api/search/alerts',
    SEARCH_SIGNALS: '/api/search/signals'
}

""""
Searches for data within Trident.
@return: A tuple of (total_number_of_results, list_of_current_page_of_results)
@param cluster_name: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
@param query: The terms to search for, i.e. "192.168.100.110" or "Windows XP".
@param scope: The type of data to search (one of SEARCH_ALL, SEARCH_ASSETS, SEARCH_ALERTS, or SEARCH_SIGNALS).
@param sort_by: How to sort the results.
@param offset: The offset at which to begin returning results. Used together with limit to page through search results.
@param limit: Number of results to return in this request. Used together with offset to page through search results.
"""
def search(cluster_name, username, api_key, query, scope=SEARCH_ALL, sort_by='-timestamp',  offset=0, limit=1000):
    if not scope:
        log.debug('search scope not set, defaulting to all')
        scope = SEARCH_ALL
    if scope not in _search_types:
        log.error('Unsupported search scope: %s', scope)
        raise ValueError('Unsupported search scope: %s' % scope)
    if not query:
        log.error('Missing query')
        raise ValueError('Missing query')
    validate_basic_params(cluster_name, username, api_key)
    url = 'https://%s%s' % (cluster_name, _search_uris[scope])
    params = {
        'q': query,
        'offset': offset,
        'limit': limit,
        'sort_by': sort_by,
        'username': username,
        'api_key': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    parsed = response.json()
    return parsed.get('meta', {}).get('total', 0), parsed.get('objects', [])

"""
Get full details of an individual search result.
@return: A dict representation of the record.
@param cluster_name: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
@param resource_uri: The resource_uri of the search result.
"""
def get_details(cluster_name, username, api_key, resource_uri):
    if not resource_uri:
        log.error('Missing resource_uri')
        raise ValueError('Missing resource_uri')
    validate_basic_params(cluster_name, username, api_key)
    params = {
        'username': username,
        'api_key': api_key
    }
    url = 'https://%s%s' % (cluster_name, resource_uri)
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
