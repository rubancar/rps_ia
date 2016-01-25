import random, copy, Queue

class Nodo(object):
    auto_incre = 0

    def __init__(self, padre=None, id=-1, arcos=[], nodos=[]):
        #self.ref_a_auto_incre = auto_incre
        #self.auto_incre += 1
        print "auto_incre",self.auto_incre
        self.id = copy.copy(self.auto_incre)
        self.hijos = {'R': None, 'S': None, 'P': None}
        self.pesos = {'R':0, 'S':0, 'P':0}
        if padre is not None:
            self.profundidad = padre.profundidad + 1
        else:
            self.profundidad = 0

    def nueva_jugada(self, cadena):
        print "cadena1",cadena
        ultimo = cadena[0]
        if len(cadena) > 1:
            if self.hijos[ultimo] is None:
                #n = Nodo(self, id=self.id+1)
                #n.auto_incre += 1
                self.hijos[ultimo] = Nodo(self, id=self.id+1)
            self.hijos[ultimo].nueva_jugada(cadena[1:])
        else:
            print "sumamos a:",ultimo," en nivel",self.profundidad,"valor",self.pesos[ultimo]
            self.pesos[ultimo] +=  1
            print "valor,",self.pesos[ultimo]

    def predecir(self, cadena):
        if len(cadena) > 0:
            ultimo = cadena[0]
            if self.hijos[ultimo] is not None:
                return self.hijos[ultimo].predecir(cadena[1:])
            else:
                return None
        else:
            return self.pesos

    def retorna_arcos(self, padre, inicio = 0):
        #if inicio = 1:
        s = ""
        if self.hijos['R'] != None:
            s += padre+'->R,'+self.retorna_arcos('R')
        if self.hijos['P'] != None:
            s += padre+'->P,'+self.retorna_arcos('P')
        if self.hijos['S'] != None:
            s += padre+'->S,'+self.retorna_arcos('S')
            #retorno el ultimo hijo
        return s


    def __str__(self):
        if self.hijos['R'] != None:
            print self.hijos['R']
        if self.hijos['S'] != None:
            print self.hijos['S']
        if self.hijos['P'] != None:
            print self.hijos['P']
        return "profundidad "+str(self.profundidad)+" id:"+str(self.id)+" distribucion R:"+str(self.pesos['R'])+" S:"+str(self.pesos['S'])+" P:"+str(self.pesos['P'])
        

class Arbol(object):
    def __init__(self):
        self.auto_incremento_id = 0
        self.arcos = []
        self.nodos = {}
        self.raiz = Nodo(id=self.auto_incremento_id, arcos=self.arcos, nodos=self.nodos)
        self.cadena = ''


    def nueva_jugada(self, cadena):
        self.cadena += cadena
        if len(self.cadena) > 10:
            self.cadena = self.cadena[-10:]

        for i in xrange(1,len(self.cadena)+1):
            print "for de nueva_juagada"
            self.raiz.nueva_jugada(self.cadena[-i:])

    def predecir(self):
        resultado = {'R':0,'S':0,'P':0}
        for i in xrange(1, len(self.cadena)+1):
            res = self.raiz.predecir(self.cadena[-i:])
            if res is not None:
                for x in res:
                    #mientras mas abajo me encuentro en el arbol el resultado obtiene un mayor peso
                    #al estar elevado a la potecia i (profundidad del arbol)
                    resultado[x] += res[x] * (1.5**i)
        r = resultado
        print "RESULTADO",resultado
        e = r.keys()
        #estoy diciendo como comparar, en este caso se comparan valores de claves diferentes
        #retorna valor mayor, al final (-1)
        e.sort(cmp=lambda a,b: cmp(r[a],r[b]))
        return e[-1]

    def imprimir_arcos(self):
        print self.raiz.retorna_arcos('0')

    def imprimir_arbol(self):
        print self.raiz

    def recorrer_arbol(self, nodo):
        self.visitados.append(nodo)
        if self.raiz.hijos['R'] != None:
            self.recorrer_arbol(self.raiz.hijos['R'])
        if self.raiz.hijos['S'] != None:
            self.recorrer_arbol(self.raiz.hijos['S'])
        if self.raiz.hijos['P'] != None:
            self.recorrer_arbol(self.raiz.hijos['P'])
        return

    '''
    Breadth first para obtener los nodos y arcos de la estructura,
    retorna el numero de nodos del arbol
    '''
    def obtener_arcos(self):
        id_unico = 0
        self.nodos = {}
        self.arcos = []
        q = Queue.Queue()
        q.put(self.raiz)
        while q.qsize():#:
            #print "while"
            actual = q.get(block=False)
            print actual
            try:
                aux = self.nodos[actual]
            except KeyError, e:
                #print "agrega nodo"
                self.nodos[actual] = id_unico
                id_unico = id_unico + 1
            for clave, nodo in actual.hijos.items():
                #print "dentro de for"
                if nodo != None:
                    #print "crea arco"
                    self.arcos.append([actual,nodo])
                    q.put(nodo)
        return id_unico



    def auto_incremento_id(self):
        self.auto_incremento_id += 1
