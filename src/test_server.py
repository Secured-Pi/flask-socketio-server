#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Testing for Flask-SocketIO server."""
import json
from server import server
import unittest


class ServerTestCase(unittest.TestCase):
    """Server test case."""
    def setUp(self):
        self.client = server.test_client()

    def tearDown(self):
        pass

    def test_socketio_channel_get_prohibited(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 405)
        self.assertTrue(b'Method Not Allowed' in res.get_data())

    def test_socketio_channel_post_return_json_with_correct_json(self):
        data = json.dumps({
            'action': 'unlock'
        })
        res = self.client.post('/', data=data, content_type='application/json')
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        self.assertTrue(res_data['sent'] is True)
        self.assertTrue('Success' in res_data['message'])

    def test_socketio_channel_post_return_json_with_wrong_json(self):
        data = json.dumps({})
        res = self.client.post('/', data=data, content_type='application/json')
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        self.assertTrue(res_data['sent'] is False)
        self.assertTrue('No action found' in res_data['message'])

if __name__ == '__main__':
    unittest.main()
