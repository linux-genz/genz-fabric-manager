#!/usr/bin/python3
import os
import random
import unittest
from pdb import set_trace
import flask
import json
from pprint import pprint

from fabric_manager import FMServer
from app_test import AppTesting


class TestDeviceBp(AppTesting):

    def test_subscribe_add_alias(self):
        app = FMServer('fm_test', cfg=self.CONFIG_PATH)
        body = {
            'callback' : 'http://localhost:1234/callback_url',
            'alias' : 'localhost'
        }

        url = 'subscribe/add_event'

        result = None
        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(body['alias'] in app.add_callback)
        self.assertTrue(result.status_code < 300)


    def test_subscribe_add_noalias(self):
        app = FMServer('fm_test', cfg=self.CONFIG_PATH)
        body = {
            'callback' : 'http://localhost:1234/callback_url',
        }

        url = 'subscribe/add_event'

        result = None
        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(body['callback'] in app.add_callback)
        self.assertTrue(result.status_code < 300)


    def test_subscribe_add_duplicate(self):
        app = FMServer('fm_test', cfg=self.CONFIG_PATH)
        body = {
            'callback' : 'http://localhost:1234/callback_url',
        }

        url = 'subscribe/add_event'

        result = None
        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(body['callback'] in app.add_callback)
        self.assertTrue(result.status_code < 300)

        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(result.status_code == 403)


    def test_subscribe_add_duplicate_alias(self):
        app = FMServer('fm_test', cfg=self.CONFIG_PATH)
        body = {
            'callback' : 'http://localhost:1234/callback_url',
            'alias' : 'localhost'
        }

        url = 'subscribe/add_event'

        result = None
        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(body['alias'] in app.add_callback)
        self.assertTrue(result.status_code < 300)

        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(result.status_code == 403)

        body['alias'] = 'anything else'
        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(result.status_code == 403)

        del body['alias']
        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body), content_type='application/json')

        self.assertTrue(result.status_code == 403)


if __name__ == '__main__':
    unittest.main()
