#!/usr/bin/env python
import logging
import sys

from argparse import ArgumentParser
from trident_client import list_sensors, list_users

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = ArgumentParser(description='Sample client for checking the status of a Trident cluster.')
    parser.add_argument('--cluster', help='cluster name, i.e. customer.portal.jask.io')
    parser.add_argument('--username', help='username to use when accessing the api')
    parser.add_argument('--api_key', help='API key to authenticate with')
    args = parser.parse_args()
    sensors = list_sensors(args.cluster, args.username, args.api_key)
    for sensor in sensors:
        print('Sensor name: %s version: %s records per second: %s last updated: %s' %
            (sensor['sensor_name'], sensor['version'], sensor['records_per_second'], sensor['last_seen']))
    users = list_users(args.cluster, args.username, args.api_key)
    for user in users:
        print('User username: %s last active: %s' % (user['username'], user['last_active']))
