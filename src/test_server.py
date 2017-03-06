#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Testing for Flask-SocketIO server."""
from server import server, io
import coverage
import unittest
import json

cover = coverage.coverage(branch=True)


class FlaskServerTestCase(unittest.TestCase):
    """Server test case."""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client = server.test_client()
        self.io_client = io.test_client(server)

    def tearDown(self):
        pass

    def test_socketio_channel_get_prohibited(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 405)
        self.assertTrue(b'Method Not Allowed' in res.get_data())

    def test_socketio_channel_post_return_json_with_correct_json(self):
        data = json.dumps({
            'serial': 'randomserial',
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
        self.assertTrue('Invalid POST data' in res_data['message'])

    def test_io_conntection(self):
        received = self.io_client.get_received()
        self.assertEqual(received[0]['args'], 'Connected!')

    def test_io_listenting_matching_serialnumber(self):
        self.io_client.emit('listening', {'serial': 'randomserial'})
        data = json.dumps({
            'serial': 'randomserial',
            'action': 'unlock'
        })
        self.client.post('/', data=data, content_type='application/json')
        received = self.io_client.get_received()[1]['args'][0]
        self.assertEqual(len(received), 2)
        self.assertEqual(received['action'], 'unlock')
        self.assertEqual(received['serial'], 'randomserial')

    def test_io_listenting_wrong_serialnumber(self):
        self.io_client.emit('listening', {'serial': 'randomserial1'})
        data = json.dumps({
            'serial': 'randomserial',
            'action': 'unlock'
        })
        self.client.post('/', data=data, content_type='application/json')
        received = self.io_client.get_received()
        self.assertEqual(len(received), 1)

if __name__ == '__main__':
    unittest.main()
