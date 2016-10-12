#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room

server = Flask(__name__)
io = SocketIO(server)


@server.route('/', methods=['POST'])
def socketio_channel():
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
    return jsonify({
        'sent': is_sent,
        'message': message,
    })


@io.on('listening')
def join(data):
    join_room(data['serial'])


if __name__ == '__main__':
    io.run(server, port=5000, host='localhost', debug=True)
