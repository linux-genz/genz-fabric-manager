#!/usr/bin/python3
import os
import random
import unittest
from pdb import set_trace
import flask
import json

from fabric_manager import FMServer
from app_test import AppTesting


class TestResourceBP(AppTesting):

    CALLBACK = {
        'callback' : 'http://localhost:1234/some/endpoint'
    }


    def test_add_cmp(self):
        print('\n----- TestResourceBP: test_add_cmp ----')
        app = FMServer('fm_test', cfg=self.CONFIG_PATH)
        sub_url = 'subscribe/add_event'
        url = 'resource/create'

        body = self.get_resource()
        body['endpoint'] = [self.CALLBACK['callback']]

        result = None
        with app.test_client() as cli:
            result = cli.post(sub_url, data=json.dumps(self.CALLBACK),
                                                content_type='application/json')

            self.assertTrue(result.status_code < 300,
                        'Failed to subscribe? Status code %s' % result.status_code)

            result = cli.post(url, data=json.dumps(body),
                                                content_type='application/json')

        self.assertTrue(result.status_code < 300,
                        'Status code %s' % result.status_code)


    def get_resource(self):
        memory = {
            'start': 281476859953152,
            'length': 0x40000000,
            'type': 0x0, #FIXME: hardcoded because reasons.Fabric Manager will figure it out
            "cclass": 11, # block storage (non-boot)
        }#memory

        resource = {
            'gcid': 1,
            'cclass': 9, # block storage (non-boot)
            'fabric': 5,
            'mgr_uuid': '9af8190f-1b4c-4be8-8732-e8d48e883396',
            'fru_uuid': '00000000-0000-0000-0000-000000000000',

            'resources': {
                'class_uuid': '3cb8d3bd-51ba-4586-835f-3548789dd906',
                'instance_uuid': '00000010-35c5-4bce-beed-614c026b2ac0',
                'class': 17, #FIXME: hardcoded because reasons.Fabric Manager will figure it out
                'memory': [memory]
            },
        }#data

        return {
            'endpoint' : ['localhost'],
            'resource' : resource
        }


if __name__ == '__main__':
    unittest.main()
