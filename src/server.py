#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_socketio import SocketIO

server = Flask(__name__)
socketio = SocketIO(server)


@server.route('/', methods=['POST'])
def socketio_channel():
    try:
        action = request.get_json()['action']
        socketio.emit(action)
        is_sent = True
        message = 'Success'
    except KeyError:
        is_sent = False
        message = 'No action found, check your json'
    return jsonify({
        'sent': is_sent,
        'message': message,
    })


if __name__ == '__main__':
    socketio.run(server, port=5000, host='localhost', debug=True)
