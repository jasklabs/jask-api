#!/usr/bin/env python
import logging, sys

from argparse import ArgumentParser

from trident_client.configuration_api import add_network_blocks_from_csv

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = ArgumentParser(description='Import internal network blocks into a Trident cluster.')
    parser.add_argument('--cluster', help='cluster name, i.e. demo.portal.jask.io')
    parser.add_argument('--username', help='username to use when accessing the api')
    parser.add_argument('--api_key', help='api key to authenticate with')
    parser.add_argument('--file', help='csv file from which to import network blocks')
    args = parser.parse_args()
    add_network_blocks_from_csv(args.cluster, args.username, args.api_key, args.file)

