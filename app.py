#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
'''
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()
'''
#import time
#from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
global cadena
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app, async_mode=async_mode)
socketio = SocketIO(app)
thread = None
cadena = []

'''
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        test_propio = 'test'
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count, 'test':test_propio},
                      namespace='/test')

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')
'''

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('piedra', namespace='/test')
def piedra(message):
    cadena.append('R')
    emit('my response', {'data': 'piedra', 'count': 0})

@socketio.on('papel', namespace='/test')
def papel(message):
    cadena.append('P')
    emit('my response', {'data': 'papel', 'count': 0})

@socketio.on('tijera', namespace='/test')
def tijera(message):
    cadena.append('S')
    emit('my response', {'data': 'tijera', 'count': 0})

@socketio.on('obtener cadena', namespace='/test')
def obtener_cadena():
    emit('my response', {'data': cadena, 'count': 0})

@socketio.on('reset juego', namespace='/test')
def obtener_cadena():
    del cadena[:]
    emit('my response', {'data': cadena, 'count': 0})

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)