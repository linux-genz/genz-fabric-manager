#!/usr/bin/python3
import argparse
import os
import json
import requests
import logging

#https://github.com/FabricAttachedMemory/flask-api-template.git
import flask_fat
from flask_fat import ConfigBuilder

logging.basicConfig(level=logging.DEBUG)


class FMServer(flask_fat.APIBaseline):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_callback = {}


def cmd_add(**args):
    from datetime import datetime
    url = 'http://localhost:1234/add/add'
    data = {
        'timestamp' : datetime.now()
    }
    data.update(args)
    resp = requests.post(url, data)
    if resp is None:
        return {}
    return json.loads(resp.text).get('data', {})


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore',
                        help='blueprints to be ignored/not-loaded by server. ' +\
                            '--ignore "bp1,bp2,bp2"', default=None)
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')
    parser.add_argument('-c', '--cfg', default=None,
                            help='Path to the RestAPI server config.')
    parser.add_argument('--logging-cfg', default=None,
                            help='Path to a python3.logging config.')

    parsed = parser.parse_args()
    if parsed.ignore is not None:
        parsed.ignore = parsed.ignore.replace(' ', '').split(',')
    return vars(parsed)


def main(args=None):
    args = {} if args is None else args
    cmd = parse_cmd()
    args.update(cmd)

    mainapp = FMServer('FabricManagerServer', **args)
    if args.get('verbose', False):
        for endpoint in mainapp.app.url_map.iter_rules():
            logging.info(endpoint.rule)

    if not args.get('dont_run', False):
        mainapp.run()
    return mainapp


if __name__ == '__main__':
    main()
