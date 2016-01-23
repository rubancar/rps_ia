#!/usr/bin/env python
import random, copy
SIZE = 4
WEIGHT_FACTOR = 7.
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
from rps import HistoryTree




app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#iniciamos varibales para juego


def iniciar_juego():
	global cadena, arbol_de_juego_pc, arbol_de_juego_user, salida, meta_predictor, metascore, \
	  gana, pierde, prediccion_pc_por_nivel, prediccion_user_por_nivel, jugadas, mapeo, y
	arbol_de_juego_pc = HistoryTree()
	arbol_de_juego_user = HistoryTree()
	salida = random.choice(["R", "P", "S"])
	y = salida
	meta_predictor = [salida] * (6 * SIZE + 6)
	metascore = [0] * (6 * SIZE + 6)
	gana = ['RS', 'SP', 'PR']
	pierde = ['SR', 'PS', 'RP']
	prediccion_pc_por_nivel = [salida] * SIZE
	prediccion_user_por_nivel = [salida] * SIZE
	jugadas = ['R', 'P', 'S']
	mapeo = {'R':'Piedra','P':'Papel','S':'Tijera'}

iniciar_juego()

def obtener_respuesta(x):
	global salida
	print "antes de copia",salida
	#global ultima
	ultima = salida

	for idx in xrange(len(metascore)):
		if meta_predictor[idx] + x in gana:
			metascore[idx] = metascore[idx] * 0.9 + 1
		elif meta_predictor[idx] + x in pierde:
			metascore[idx] = metascore[idx] * 0.9 - 1
		else:
			metascore[idx] = metascore[idx] * 0.9 - 0.34
	#realiza una prediccion recorriendo todo el arbol
	prediccion_pc = arbol_de_juego_user.predict()
	prediccion_user = arbol_de_juego_pc.predict()
	#realiza una prediccion 
	for j in xrange(SIZE):
		prediccion_pc_por_nivel[j] = arbol_de_juego_pc.predict_i(j)
		prediccion_user_por_nivel[j] = arbol_de_juego_user.predict_i(j)
		
	for i in xrange(3):
		jugada_pc = jugadas[(jugadas.index(prediccion_pc) + i) % 3]
		jugada_user = jugadas[(jugadas.index(prediccion_user) + i) % 3]
		meta_predictor[i] = jugada_pc
		meta_predictor[i + 3] = jugada_user
		for j in xrange(SIZE):
			jugada_pc = jugadas[(jugadas.index(prediccion_pc_por_nivel[j]) + i) % 3]
			jugada_user = jugadas[(jugadas.index(prediccion_user_por_nivel[j]) + i) % 3]
			meta_predictor[i + (j + 1) * 6] = jugada_pc
			meta_predictor[i + 3 + (j + 1) * 6] = jugada_user

	best_predictor = metascore.index(max(metascore))

	play_random = True
	for score in metascore:
		#significa que el score ha ganado 3 veces seguidas
		if score > 2.7:
			play_random = False
	if play_random:
		salida = random.choice(["R", "P", "S"])
		#print "maquina-random:",salida
	else:
		salida = meta_predictor[best_predictor]
		#print "maquina:",salida
	print 'salida_final',salida
	return mapeo[ultima]




@app.route('/')
def index():
	return render_template('index2.html')

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
	arbol_de_juego_pc.new_move(salida + 'R')
	arbol_de_juego_user.new_move(salida + 'R')
	emit('my response', {'user_jugada': 'Piedra', 'pc_jugada':obtener_respuesta('R')})

@socketio.on('papel', namespace='/test')
def papel(message):
	arbol_de_juego_pc.new_move(salida + 'P')
	arbol_de_juego_user.new_move(salida + 'P')
	emit('my response', {'user_jugada': 'Papel', 'pc_jugada':obtener_respuesta('P')})

@socketio.on('tijera', namespace='/test')
def tijera(message):
	arbol_de_juego_pc.new_move(salida + 'S')
	arbol_de_juego_user.new_move(salida + 'S')
	emit('my response', {'user_jugada': 'Tijera', 'pc_jugada':obtener_respuesta('S')})

@socketio.on('obtener cadena', namespace='/test')
def obtener_cadena():
	emit('my response', { 'count': 0})

@socketio.on('reset juego', namespace='/test')
def reset_juego():
	iniciar_juego()
	emit('my response', {'data': "juego reseteado"})

@socketio.on('obtener arbol', namespace='/test')
def obtener_arbol():
	#se envia estructura (id, jugada, valor)
	nodos = [(0,'R',1),(1,'R',2),(2,'P',2),(3,'S',2),(4,'R',2),(5,'S',3)]
	arcos = [(0,1),(0,3),(1,4),(3,5),(4,3),(4,5)]
	emit('arbol',{'nodos':nodos, 'arcos':arcos})

@socketio.on('connect', namespace='/test')
def test_connect():
	emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	print('Client disconnected', request.sid)


if __name__ == '__main__':
	socketio.run(app, debug=True, port=5000)



