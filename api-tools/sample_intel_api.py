#!/usr/bin/env python
import logging, sys

from argparse import ArgumentParser
from trident_client.intel_api import threat_intel_from_csv

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = ArgumentParser(description='Import threat intelligence into a Trident cluster.')
    parser.add_argument('--cluster', help='cluster name, i.e. demo.portal.jask.io')
    parser.add_argument('--username', help='username to use when accessing the api')
    parser.add_argument('--api_key', help='password to authenticate with')
    parser.add_argument('--file', help='file from which to import indicators')
    parser.add_argument('--confidence', help='Confidence in the indicator - High/Medium/Low')
    args = parser.parse_args()
    threat_intel_from_csv(args.cluster, args.username, args.api_key, args.file, args.confidence)
