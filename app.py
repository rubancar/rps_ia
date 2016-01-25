#!/usr/bin/env python
import random, copy
import operator
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
from rps import Arbol
from rps_genetico import RPSGenetico


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


def empezar_juego_ga():
	global juego_ga
	juego_ga = RPSGenetico()

def predecir_respuesta_genetica():
	global fenotipo, fitness
	fenotipo = juego_ga.mejor_fenotipo
	fitness = juego_ga.fitness
	return juego_ga.obtener_jugada()

#iniciamos varibales para juego
def empezar_juego():
	global cadena, arbol_pc, arbol_jugador, salida, mejor_predictor, gana, pierde, \
	prediccion_pc, prediccion_jugador, mapeo, opciones, todas_predicciones, nodos_x, arcos_x, estrategia
	arbol_pc = Arbol()
	arbol_jugador = Arbol()
	salida = random.choice(["R", "P", "S"])
	todas_predicciones = [salida] * 6
	mejor_predictor = [0] * 6
	gana = ['RS', 'SP', 'PR']
	pierde = ['SR', 'PS', 'RP']
	opciones = ['R','P','S']
	mapeo = {'R':'Piedra','P':'Papel','S':'Tijera'}
	nodos_x = []
	arcos_x = []

#empezar_juego()

def predecir_respuesta(nueva_jugada, prediccion_y_jugada=True):
	global salida, nodos_x, arcos_x, estrategia
	del arcos_x[:]
	del nodos_x[:]
	ultima = salida
	'''
	Seleccionamos el mejor predictor, de las 6 estrategias, basado en un disenio heuristico llamado
	(Iocaine Powder) http://dan.egnor.name/iocaine.html
	'''
	if prediccion_y_jugada:
		for i in xrange(len(mejor_predictor)):
			if todas_predicciones[i] + nueva_jugada in gana:
				mejor_predictor[i] = mejor_predictor[i]  + 1
			elif todas_predicciones[i] + nueva_jugada in pierde:
				mejor_predictor[i] = mejor_predictor[i] - 1
			else:
				mejor_predictor[i] = mejor_predictor[i]  - 0.34

	prediccion_pc = arbol_pc.predecir()
	prediccion_jugador = arbol_jugador.predecir()
	print "ESTAAAAAAAA ES LA QUE VA A USAR HPPP:",prediccion_jugador
	# 1) jugar estrategia propia (maquina)
	todas_predicciones[0] = prediccion_pc
	# 2) ponerme en los zapatos del jugador (adivinando) y jugar para vencer
	todas_predicciones[1] = opciones[(opciones.index(prediccion_jugador) + 1) % 3]
	# 3) rotar 1) por dos y jugar movimiento que lo hace perder 
	todas_predicciones[2] = opciones[(opciones.index(prediccion_pc) + 2) % 3]
	# 4) rotar 2) por dos, es lo mismo que 3)
	todas_predicciones[3] = opciones[(opciones.index(prediccion_pc) + 2) % 3]
	# 5) rotar 3) por dos
	todas_predicciones[4] = opciones[(opciones.index(todas_predicciones[2]) + 2) % 3]
	# 6) rotar 4) por dos
	todas_predicciones[5] = opciones[(opciones.index(todas_predicciones[3]) + 2) % 3]

	a_jugar = mejor_predictor.index(max(mejor_predictor))
	jugar_aleatorio = True
	for predictor in mejor_predictor:
		#significa que el score ha ganado 3 veces seguidas
		if predictor > 1:
			jugar_aleatorio = False
	if jugar_aleatorio:
		print "ESTRATEGIA RANDOM"
		salida = random.choice(["R", "P", "S"])
		estrategia = 'random'
	else:
		print "ESTRATEGIA #", a_jugar+1
		salida = todas_predicciones[a_jugar]
		estrategia = a_jugar+1
	print 'salida_final',salida
	nodos = arbol_jugador.obtener_arcos()
	sorted_x = sorted(arbol_jugador.nodos.items(), key=operator.itemgetter(1))
	nodos_x = []
	arcos_x = []
	#creamos la estructura que retorna los nodos
	for elemento in sorted_x:
		nodo = elemento[0]
		id_nodo = elemento[1]
		r = nodo.pesos['R']
		s = nodo.pesos['S']
		p = nodo.pesos['P']
		nodos_x.append((id_nodo, r, s, p))
		#for k, v in nodo.pesos.items():
		#	if v != 0:
		#		nodos_x.append((id_nodo, k, v))
	#creamos la estructura que retorna los arcos
	for arco in arbol_jugador.arcos:
		inicio, fin = arco
		arcos_x.append((arbol_jugador.nodos[inicio],arbol_jugador.nodos[fin]))

	print "nodos",nodos_x
	#vaciamos nodos_x para una proxima consulta
	#del nodos_x[:]
	print "arcos",arcos_x
	#del arcos_x[:]
	arbol_jugador.imprimir_arbol()
	#print 'ARBOL:',arbol_jugador.imprimir_arbol()
	#arbol_jugador.recorrer_arbol(arbol_jugador.raiz)
	#arbol_jugador.visitados = []
	#print 'arcos',arbol_jugador.imprimir_arcos()
	return mapeo[ultima]

def mi_jugada(v):
	if v=='R' or v=='Piedra':
		return 'Papel'
	elif v=='P' or v=='Papel':
		return 'Tijera'
	elif v=='S' or v=='Tijera':
		return 'Piedra'

def mapeo_a_inicial(v):
	if v == 'Piedra':
		return 'R'
	elif v == 'Papel':
		return 'P'
	elif v == 'Tijera':
		return 'S'

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
	predic = predecir_respuesta('R')
	arbol_pc.nueva_jugada('R')
	arbol_jugador.nueva_jugada('R')
	emit('my response', {'user_jugada': 'Piedra', 'pc_jugada':mi_jugada(predic), 'estrategia':'estrategia'})

@socketio.on('papel', namespace='/test')
def papel(message):
	predic = predecir_respuesta('P')
	arbol_pc.nueva_jugada('P')
	arbol_jugador.nueva_jugada('P')
	emit('my response', {'user_jugada': 'Papel', 'pc_jugada':mi_jugada(predic), 'estrategia':'estrategia'})

@socketio.on('tijera', namespace='/test')
def tijera(message):
	predic = predecir_respuesta('S')
	arbol_pc.nueva_jugada('S')
	arbol_jugador.nueva_jugada('S')
	emit('my response', {'user_jugada': 'Tijera', 'pc_jugada':mi_jugada(predic), 'estrategia':'estrategia'})

@socketio.on('obtener cadena', namespace='/test')
def obtener_cadena():
	emit('my response', { 'count': 0})

@socketio.on('reset juego', namespace='/test')
def reset_juego():
	empezar_juego()
	emit('my response', {'data': "juego reseteado con arbol de caminos"})

@socketio.on('iniciar ga', namespace='/test')
def reset_juego_ga():
	empezar_juego_ga()
	emit('my response', {'data': "juego reseteado con ga"})

@socketio.on('jugar genetico', namespace='/test')
def jugar_genetico(message):
	jugada = message["data"]
	predic = predecir_respuesta_genetica()
	juego_ga.agregar_jugada(mapeo_a_inicial(jugada))
	print "jugada en ga user:",jugada
	emit('my response', {'user_jugada': jugada, 'pc_jugada':mi_jugada(predic), 'estrategia':'estrategia'})

@socketio.on('datos ga', namespace='/test')
def datos_ga():
	predic = predecir_respuesta_genetica()
	emit('datos geneticos', {'data': "datos ga",'prediccion':mi_jugada(predic),'fenotipo':fenotipo,'fitness':fitness})

@socketio.on('obtener arbol', namespace='/test')
def obtener_arbol():
	predic = predecir_respuesta('X',prediccion_y_jugada=False)
	#se envia estructura (id, jugada, valor)
	nodos = nodos_x
	#se envia estructura (id_source, id_target)
	arcos = arcos_x
	emit('dibujar arbol',{'nodos':nodos, 'arcos':arcos, 'prediccion':salida, 'mi_jugada':mi_jugada(salida),'estrategia':estrategia})

@socketio.on('connect', namespace='/test')
def test_connect():
	emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	print('Client disconnected', request.sid)


if __name__ == '__main__':
	socketio.run(app, debug=True, port=5000)



