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
    """
        Accepts POST request with a json body describing the resource and the
    list of endpoints (optional. Aliases or urls) to notify about the resource.
    Body model:
    {
        'endpoint' : 'array',
        'resource' : 'object'
    }

    Refere to "get_resource_schema()" for the "resource" model
    """
    global Journal
    mainapp = Journal.mainapp
    body = flask.request.get_json()

    if body is None:
        msg = { 'error ' : ''}
        return flask.make_response(flask.jsonify(msg), 400)

    resource = body.get('resource', None)
    endpoints = body.get('endpoint', [])

    # If nobody subscribed to this "create" event, then nobody will be notified.
    # TODO: save the target endpoints that has not subscribed yet and call them
    # with the shared resource once they subscribe to this event.
    if not mainapp.add_callback:
        msg = { 'error' : 'Nothing happened. There are No subscribers to this event, yet.' }
        return flask.make_response(flask.jsonify(msg), 304)

    # Gets the list of endpoint targets to share resource with.
    endpoints = extract_target_endpoints(endpoints, mainapp.add_callback)

    if not mainapp.add_callback:
        msg = { 'error' : 'Targeted endpoints not found in the subscription list!' }
        return flask.make_response(flask.jsonify(msg), 404)

    resp = send_resource(resource, endpoints)

    return resp


def send_resource(resource: dict, endpoints: list):
    """
        Makes an http call to each of the the "endpoints" urls.

        @return: a flask response object (with jsonified msg, status code and etc).
    """
    response = {}
    response['callback'] = {'failed': [], 'success': []}

    if resource is None:
        response['error'] = 'Missing "resource" object in the body! (the one describing the resource..)'
        return flask.make_response(flask.jsonify(response), 400)

    try:
        jsonschema.validate(resource, schema=get_resource_schema())
    except Exception as err:
        response['error'] = str(err)
        return flask.make_response(flask.jsonify(response), 400)

    for endpoint in endpoints:
        try:
            msg = HTTP_REQUESTS.post(endpoint, data=json.dumps(resource), content_type='application/json')
            if msg.status_code < 300:
                response['callback']['success'].append(endpoint)
            else:
                response['callback']['failed'].append(endpoint)
                response['error'] = msg.reason
        except Exception as err:
            if 'error' not in response:
                response['error'] = {}
            response['error'] = str(err)

    return flask.make_response(flask.jsonify(response), 200)


def extract_target_endpoints(targets, known):
    """
        There are subscribed endpoints (@known) and there are targets that a user
    wants to share the resource with. This function gets a "union" of the two and
    will return only those targets that are in the known state.

        @param targets: a list of urls or aliases to get urls from the the subscription list.
        @param known: a subscription dictionary of { 'alias' : 'url' } pair.
    """
    if not targets:
        return known.values()

    result = []
    for target in targets:
        url = None

        #Check for the Alias match
        if target in known:
            url = known[target]

        #Check for URL match
        if url is None and target in known.values():
            url = target

        if url is not None:
            result.append(url)

    return result


def get_resource_schema():
    """
        The Resource schema that is sent in the body by the resource creator and
    which is understood by LLamas service.
    """
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