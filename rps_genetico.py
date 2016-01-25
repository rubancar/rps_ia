ROCK = 'R'
PAPER = 'P'
SCISSORS = 'S'
import random


class RPSGenetico():
	def __init__(self, tamanio_generacion = 10, tamanio_fenotipo = 3, factor_mutacion = 0.1):
		self.generacion_actual = None #Generacion(tamanio_generacion, tamanio_fenotipo, factor_mutacion, 1)
		self.ganados = 0
		self.perdidos = 0
		self.empatados = 0
		self.cadena = ""
		self.movimiento_actual = random.choice((ROCK, PAPER, SCISSORS))
		self.vieja_mejor_generacion = None
		self.ganan = ('RS','SP','PR')
		self.pierden = ('SR','PS','RP')
		self.vence = {'R':'P','S':'R','P':'S'}
		self.mejor_fenotipo = None
		self.fitness = None

	def agregar_jugada(self, mov):
		self.cadena += mov

	def establecer_resultado_ronda(self, mov):
		resultado = self.movimiento_actual + mov
		if resultado in self.ganan:
			self.ganados += 1
		elif resultado in self.pierden:
			self.perdidos += 1
		else:
			self.empatados += 1

	def obtener_jugada(self):
		if len(self.cadena) < 3:
			return random.choice((ROCK, PAPER, SCISSORS))
		else:
			self.generacion_actual =  Generacion(pow(len(self.cadena),2), len(self.cadena), 0.1, 1, self.vieja_mejor_generacion)
			if self.vieja_mejor_generacion == None:
				self.generacion_actual.nueva_generacion_aleatoria()
			else:
				self.generacion_actual.nueva_generacion(len(self.cadena))
			self.generacion_actual.establecer_mejores_individuos(self.cadena)
			while self.generacion_actual.calidad_de_generacion() < 0.18:
				#print "calidad",self.generacion_actual.calidad_de_generacion()
				self.generacion_actual = self.generacion_actual.evolucion_de_generacion()
				self.generacion_actual.establecer_mejores_individuos(self.cadena)
			#retornamos la posible jugada
			self.vieja_mejor_generacion = self.generacion_actual.obtener_mejor_generacion()
			posible_jugada = self.generacion_actual.obtener_posible_jugada(self.cadena)
			self.mejor_fenotipo = self.generacion_actual.cadena_final
			self.fitness = self.generacion_actual.calidad_de_generacion() 
			return self.vence[posible_jugada]


'''
Clase que mantiene cada una de las generaciones generadas para el juego
'''
class Generacion():
	def __init__(self, tamanio_generacion, tamanio_fenotipo, factor_mutacion, contador_generacion, vieja_generacion):
		self.tamanio_generacion = tamanio_generacion
		self.tamanio_fenotipo = tamanio_fenotipo
		self.factor_mutacion = factor_mutacion
		self.individuos = []
		self.mejores_individuos = []
		self.calidad = 0
		self.contador_generacion = contador_generacion
		self.vieja_generacion = vieja_generacion
		self.cadena_final = None
		print "Generacion #",self.contador_generacion

	def nueva_generacion_aleatoria(self):
		self.individuos.extend([Individuo(self.tamanio_fenotipo, self.factor_mutacion) for n in range(self.tamanio_generacion)])

	def establecer_mejores_individuos(self, cadena_original):
		for individuo in self.individuos:
			#este valor quiere decir que tiene una distacia menor o igual 6
			if individuo.establecer_relevancia(cadena_original) > 0.26:
				self.mejores_individuos.append(individuo)
		print "tamanio_mejores",len(self.mejores_individuos)

	def calidad_de_generacion(self):
		acumulador = 0
		for individuo in self.individuos:
			acumulador += individuo.obtener_relevancia()
		#la calidad de la generacion es el promedio de la calidad de sus individuos
		self.calidad = acumulador/len(self.individuos)
		#print  "calidad:",self.calidad
		return self.calidad

	def evolucion_de_generacion(self):
		nueva = Generacion(self.tamanio_generacion, self.tamanio_fenotipo, self.factor_mutacion, self.contador_generacion+1, [])
		if len(self.mejores_individuos) == 0:
			print "No existieron buenos individuos en generacion",self.contador_generacion,"generamos nueva"
			nueva.nueva_generacion_aleatoria()
		else:
			for i in xrange(self.tamanio_generacion):
				individuo = Individuo(self.tamanio_fenotipo, self.factor_mutacion)
				#cruzamos 2 de los mejores hijos de forma aleatoria
				hijo_a = self.mejores_individuos[random.randrange(len(self.mejores_individuos))]
				hijo_b = self.mejores_individuos[random.randrange(len(self.mejores_individuos))]
				individuo.cruce_de_hijos(hijo_a, hijo_b)
				#individuo.mutar()
				nueva.agregar_individuo(individuo)
		return nueva


	def agregar_individuo(self, individuo):
		self.individuos.append(individuo)

	def obtener_posible_jugada(self, secuencia_de_juego):
		ordenar_mejores_hijos = sorted(self.mejores_individuos, key=lambda individuo: individuo.relevancia)
		ordenar_mejores_hijos.reverse()
		#print 
		for hijo in ordenar_mejores_hijos:
			print hijo
		#analizamos las 2 mejores cadenas y elejimos secuencias repetidas de las 2
		self.cadena_final = ordenar_mejores_hijos[0].fenotipo_como_cadena()
		posibles = []
		for i in xrange(1,4):
			sub = secuencia_de_juego[-i]
			indice = self.cadena_final.find(sub)
			print "indice",indice
			if indice != -1 and indice != (len(self.cadena_final)-1):
				posibles.append(self.cadena_final[indice+1])
		#retorno el ultimo debido a que es el mejor de todos, cadena mas larga
		if len(posibles) == 0:
			print "retorno aleatorio"
			return random.choice((ROCK, PAPER, SCISSORS))
		else:
			print "retorno NO aleatorio"
			return posibles[-1]

	def obtener_mejor_generacion(self):
		return self.mejores_individuos

	def nueva_generacion(self, tamanio_fenotipo):
		for n in xrange(self.tamanio_generacion):
			#individuo viejo a ser evolucionado para nueva generacion
			viejo = self.vieja_generacion[random.randrange(len(self.vieja_generacion))]
			nuevo = viejo.retorna_nuevo_individuo_adaptado(tamanio_fenotipo, 1)
			self.individuos.append(nuevo)


'''
Clase que mantiene cada una de las generaciones generadas para el juego
'''
class Individuo():
	"""docstring for Individuo"""
	def __init__(self, tamanio_fenotipo, factor_mutacion):
		self.tamanio_fenotipo = tamanio_fenotipo
		self.factor_mutacion = factor_mutacion
		self.relevancia = -1.0
		'''se inicia con una cadena aleatoria que luego puede variar si estamos en un proceso de crossover de hijos'''
		self.fenotipo = [random.choice((ROCK, PAPER, SCISSORS)) for v in xrange(tamanio_fenotipo)]

	'''
	Usamos distancia de levenshtein para evaluar la relevancia de cada individuo,
	su parecido a la cadena original del jugador, codigo obtenido de Wikipedia.
	'''
	def levenshtein(self, s1, s2):
		#print "cadena1",s1,"cadena2",s2
		if len(s1) < len(s2):
			return levenshtein(s2, s1)
		# len(s1) >= len(s2)
		if len(s2) == 0:
			return len(s1)
		previous_row = range(len(s2) + 1)
		for i, c1 in enumerate(s1):
			current_row = [i + 1]
			for j, c2 in enumerate(s2):
				insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
				deletions = current_row[j] + 1       # than s2
				substitutions = previous_row[j] + (c1 != c2)
				current_row.append(min(insertions, deletions, substitutions))
			previous_row = current_row
		
		return previous_row[-1]

	def establecer_relevancia(self, cadena_original):
		fenotipo_cadena = self.fenotipo_como_cadena()
		#for gen in self.fenotipo:
		#	fenotipo_cadena += gen 
		distancia = float(self.levenshtein(cadena_original, fenotipo_cadena))
		#print "distancia",distancia
		if distancia == 0:
			distancia = 1
		#la relevancia es el inverso de la distancia
		self.relevancia = float(1/distancia)
		return self.relevancia

	def cruce_de_hijos(self, hijo1, hijo2):
		#print "cruce_de_hijos"
		cruce = random.randrange(self.tamanio_fenotipo)
		for i in xrange(self.tamanio_fenotipo):
			if (i < cruce):
				hijo1.fenotipo[i] = hijo1.gen(i)
			else:
				hijo2.fenotipo[i] = hijo2.gen(i)
	
	def gen(self, indice):
		return self.fenotipo[indice]

	def obtener_relevancia(self):
		return self.relevancia

	def fenotipo_como_cadena(self):
		return ''.join(x for x in self.fenotipo)

	def retorna_nuevo_individuo_adaptado(self, tamanio_fenotipo, factor_mutacion):
		individuo = Individuo(tamanio_fenotipo, factor_mutacion)
		for i in xrange(len(self.fenotipo)):
			individuo.fenotipo[i] = self.fenotipo[i]
		for j in xrange(i, tamanio_fenotipo):
			individuo.fenotipo[i] = random.choice((ROCK, PAPER, SCISSORS))
		return individuo

	def __str__(self):
		return "fenotipo: "+self.fenotipo_como_cadena()+" relevancia: "+str(self.relevancia)