import sys
import logging

import requests
import unicodecsv as csv

from .utils import validate_basic_params, is_int_string


log = logging.getLogger()

"""
Read in threat intel csv file and post as json to cluster.
@return Nothing, will raise an exception if failed.
@param cluster: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
@param filename: The name of the threat intel csv file to be posted.
@param confidence: The default confidence level for intel from this file.
"""
def threat_intel_from_csv(cluster, username, api_key, filename, default_confidence):
    if not filename:
        log.error('Filename not specified')
        raise ValueError('Filename not specified')
    validate_basic_params(cluster, username, api_key)
    results = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        intel_fields = ['value', 'confidence', 'source', 'tags', 'ttl', 'override_ttl']
        for row in csvreader:
            (value, confidence, source, tags, ttl, override_ttl) = (row.get(f) for f in intel_fields)
            if confidence and is_int_string(confidence):
                confidence = int(confidence)
            if ttl and is_int_string(ttl):
                ttl = int(ttl)
            results.append({
                'value': value,
                'confidence': confidence or default_confidence,
                'source': source or 'User Import',
                'tags': tags.split(',') if tags else [],
                'ttl': ttl or None,
                'active': True,
                'override_ttl': True if (override_ttl and override_ttl.lower()=='true') else False
            })
    intel = {'objects': results}
    params = {'username': username, 'api_key': api_key}
    url = 'https://%s/api/intelligence' % cluster
    response = requests.post(url, json=intel, params=params)
    response.raise_for_status()
