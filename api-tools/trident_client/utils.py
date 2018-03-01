import logging, requests

log = logging.getLogger()

def validate_basic_params(cluster_name, username, api_key):
    if not cluster_name or not username or not api_key:
        msg = 'Missing one or more of cluster_name, username, and api_key'
        log.error(msg)
        raise ValueError(msg)

def get_simple_list(url, username, api_key):
    params = {
        'username': username,
        'api_key': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('objects', [])

def is_int_string(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
