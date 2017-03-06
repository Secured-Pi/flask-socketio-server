#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the Flask server module for Secured Pi.

The Flask server is responsible for 2-way communication with the Raspberry Pi,
and for receiving commands from the main Django server (such as, lock/unlock).
"""

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room, send

server = Flask(__name__)
io = SocketIO(server)


@server.route('/', methods=['POST'])
def socketio_channel():
    """Attempt to send command to RPi."""
    print('incoming post request!')
    try:
        data = request.get_json()
        io.emit(
            data['action'],
            data,
            room=data['serial']
        )
        is_sent = True
        message = 'Success'
    except KeyError:
        is_sent = False
        message = 'Invalid POST data'
    print(jsonify({'sent': is_sent, 'message': message}))
    return jsonify({'sent': is_sent, 'message': message})


@io.on('connect')
def on_connect():
    """Send connected message."""
    send('Connected!')


@io.on('listening')
def join(data):
    """Join the communication channel."""
    join_room(data['serial'])

if __name__ == '__main__':
    # io.run(server, port=5000, host='localhost', debug=True)
    io.run(server, port=5000, host='0.0.0.0', debug=True)
