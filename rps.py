import random, copy

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
        ultimo = cadena[0]
        if len(cadena) > 1:
            if self.hijos[ultimo] is None:
                n = Nodo(self, id=self.id+1)
                n.auto_incre += 1
                self.hijos[ultimo] = n
            self.hijos[ultimo].nueva_jugada(cadena[1:])
        else:
            #multiplicamos por un factor de 0.975
            self.pesos[ultimo] += self.pesos[ultimo] * 0.975 + 1

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
        self.nodos = []
        n = Nodo(id=self.auto_incremento_id, arcos=self.arcos, nodos=self.nodos)
        n.auto_incre += 1
        self.raiz = n
        self.cadena = ''


    def nueva_jugada(self, cadena):
        self.cadena += cadena
        if len(self.cadena) > 10:
            self.cadena = self.cadena[-10:]

        for i in xrange(1,len(self.cadena)+1):
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


    def auto_incremento_id(self):
        self.auto_incremento_id += 1
