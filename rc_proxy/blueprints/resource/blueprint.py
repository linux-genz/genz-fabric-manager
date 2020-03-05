#!/usr/bin/python3
import flask
import requests as HTTP_REQUESTS
import socket
import jsonschema
import json
from pdb import set_trace

import flask_fat

Journal = self = flask_fat.Journal(__file__)

""" ----------------------- ROUTES --------------------- """

@Journal.BP.route('/%s/create' % (Journal.name), methods=['POST'])
def create_resource():
    global Journal
    app = Journal.mainapp.app
    routes = []
    body = flask.request.data
    body = json.loads(body)

    if body is None:
        resp = { 'error ' : ''}
        return flask.make_response(flask.jsonify(resp), 400)

    resources = body.get('resources', None)

    if resources is None:
        resp = { 'error ' : 'Missing "daresourcesta" object in the body! (the one describing the resource..)'}
        return flask.make_response(flask.jsonify(resp), 400)

    for res in resources:
        try:
            jsonschema.validate(res, schema=get_add_schema())
        except Exception as err:
            resp = { 'error' : str(err) }
            return flask.make_response(flask.jsonify(resp), 400)


    return flask.make_response(flask.jsonify({'status' : 'success'}), 200)


def get_add_schema():
    return {
        'gcid': 'number',
        'cclass': 'number', # block storage (non-boot)
        'fabric': 'number',
        'mgr_uuid': 'string',
        'fru_uuid': 'string',
        'uuid': 'string',

        'resources': {
            'uuid': 'string',
            'class': 'number', #FIXME: hardcoded because reasons.Fabric Manager will figure it out
            'memory': {
                'start': 'number',
                'length': 'number',
                'type': 'number',
                "cclass": 'number',
            }
        },
    }