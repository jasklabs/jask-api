#!/usr/bin/env python
import logging
import sys
import unicodecsv as csv

from argparse import ArgumentParser
from pprint import PrettyPrinter
from trident_client import get_asset_detail, update_metadata, delete_metadata

log = logging.getLogger()
pprinter = PrettyPrinter(indent=1)

def get_updates_from_csv_file(csv_file, default_ip):
    results = {default_ip: None}
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset_detail = results.get(default_ip)
            row_ip = default_ip
            if 'asset_ip' in row:
                row_ip = row['asset_ip']
                asset_detail = results.get(row_ip, {})
            section_name = row.get('section')
            key = row['key']
            value = row['value']
            if section_name:
                section = asset_detail.get(section_name, {})
                section[key] = value
                asset_detail[section_name] = section
            else:
                asset_detail[key] = value
            results[row_ip] = asset_detail
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = ArgumentParser(description='Sample client for interacting with assets using the Trident API.')
    parser.add_argument('--cluster', help='cluster name, i.e. customer.portal.jask.io')
    parser.add_argument('--username', help='username to use when accessing the api')
    parser.add_argument('--api_key', help='API key to authenticate with')
    parser.add_argument('--get', help='IP address of the asset to retrieve')
    parser.add_argument('--delete', help='IP address of the asset for which metadata will be deleted')
    parser.add_argument('--update', help='IP address of the asset for which metadata will be updated. If file is specified, this may be ommitted.')
    parser.add_argument('--section', help='Name of the metadata section to update or delete. This may be ommitted when updating/deleting top-level metadata.')
    parser.add_argument('--key', help='Name of the metadata value to update or delete.')
    parser.add_argument('--file', help='CSV file of metadata to update.')
    parser.add_argument('--value', help='Single metadata value to update. Key must also be specified.')
    args = parser.parse_args()
    if args.get:
        asset = get_asset_detail(args.cluster, args.username, args.api_key, args.get)
        pprinter.pprint(asset)
    elif args.update or args.file:
        if args.update and not args.file:
            if not args.value or (not args.key and not args.file):
                log.error('Either key or file must be specified')
                sys.exit(1)
            elif args.value:
                update_metadata(args.cluster, args.username, args.api_key, args.update, {args.key: args.value}, section_name=args.section)
        elif args.file:
            updates = get_updates_from_csv_file(args.file, args.update)
            for key, value in updates.iteritems():
                if key: update_metadata(args.cluster, args.username, args.api_key, key, value)
    elif args.delete:
        delete_metadata(args.cluster, args.username, args.api_key, args.delete, section_name=args.section, key=args.key)
    else:
        log.error('One of get, delete, update, or file must be specified')
        sys.exit(1)
