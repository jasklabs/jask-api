from utils import validate_basic_params
import logging
import requests
import unicodecsv as csv

log = logging.getLogger()

def _submit_network_blocks(cluster, username, api_key, batch):
    url = 'https://%s/api/configuration/networkblock' % cluster
    params = {'username': username, 'api_key': api_key}
    response = requests.post(url, json={'objects': batch}, params=params)
    response.raise_for_status()

def add_network_blocks_from_csv(cluster, username, api_key, filename):
    if not filename:
        log.error('Filename not specified')
        raise ValueError('Filename not specified')
    validate_basic_params(cluster, username, api_key)
    batch = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            batch.append({'address_block': row.get('address_block'), 'label': row.get('label')})
            if len(batch)%25==0:
                _submit_network_blocks(cluster, username, api_key, batch)
                batch = []
        if batch: _submit_network_blocks(cluster, username, api_key, batch)
