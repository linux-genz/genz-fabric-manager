#!/usr/bin/python3
import os
import random
import unittest
from pdb import set_trace
import flask
import json

from rc_proxy import RCProxy
from app_test import AppTesting


class TestDeviceBp(AppTesting):

    def test_add_cmp(self):
        app = RCProxy('rcproxy_test', cfg=self.CONFIG_PATH)
        url = 'resource/create'

        memory = {
            'start': 281476859953152,
            'length': 0x40000000,
            'type': 0x0, #FIXME: hardcoded because reasons.Fabric Manager will figure it out
            "cclass": 11, # block storage (non-boot)
        }#memory

        data = {
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
        body = { 'resources' : [data] }

        result = None
        with app.test_client() as cli:
            result = cli.post(url, data=json.dumps(body))

        self.assertTrue(result.status_code < 300,
                        'Status code %s' % result.status_code)
        print('\n----- TestDeviceBp: test_add_cmp ----')
        print(result.json)


if __name__ == '__main__':
    unittest.main()
