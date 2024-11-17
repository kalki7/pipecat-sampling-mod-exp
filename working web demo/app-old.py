from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for all origins

@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('broadcast')
def handle_broadcast_event(msg):
    send(msg, broadcast=True)

@socketio.on('custom_event')
def handle_custom_event(data):
    emit('response', {'data': 'Custom event received!'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8765)
