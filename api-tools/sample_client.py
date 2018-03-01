#!/usr/bin/env python
import logging
import sys

from argparse import ArgumentParser
from pprint import PrettyPrinter
from trident_client import search, get_details

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = ArgumentParser(description='Sample client for searching with the Trident API.')
    parser.add_argument('--cluster', help='cluster name, i.e. customer.portal.jask.io')
    parser.add_argument('--username', help='username to use when accessing the api')
    parser.add_argument('--api_key', help='API key to authenticate with')
    parser.add_argument('--search_type', help='type of record to search (one of: alert, asset, signal, all)')
    parser.add_argument('--query', help='the search query')
    parser.add_argument('--detail', dest='detail', action='store_true')
    parser.add_argument('--offset', dest='offset')
    parser.add_argument('--limit', dest='limit')
    parser.add_argument('--id', dest='id', help='UUID of an single alert, signal, or asset to return')
    args = parser.parse_args()
    pprinter = PrettyPrinter(indent=1)
    offset = args.offset or 0
    limit = args.limit or 1000
    if args.id:
    	args.query = 'id:' + args.id
    (number_of_results, results) = search(args.cluster, args.username, args.api_key, args.query, scope=args.search_type,  offset=offset, limit=limit)
    print('\nThere are %s total results\n' % number_of_results)
    for result in results:
        if not args.detail:
            print('Timestamp:   %s' % result['timestamp'])
            print('Asset:       %s' % result['asset'].get('ip'))
            print('Description: %s' % result.get('description', ''))
            print('Result Type: %s' % result['doc_type'])
            print('Result ID:   %s' % result['id'])
            print('=============')
        else:
            detail = get_details(args.cluster, args.username, args.api_key, result['resource_uri'])
            pprinter.pprint(detail)
