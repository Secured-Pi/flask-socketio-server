#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple SocketIO server that maintains RPi connections."""

from flask import Flask, jsonify, request
from flask_socketio import SocketIO

server = Flask(__name__)
socketio = SocketIO(server)


@server.route('/')
def socketio_channel():
    message = request.json()
    return jsonify({'result': message})

if __name__ == '__main__':
    socketio.run(server)
