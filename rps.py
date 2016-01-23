import random

SIZE = 4
WEIGHT_FACTOR = 7.

class HistoryNode(object):
    def __init__(self, parent=None):
        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        self.children = {'RR': None, 'RS': None, 'RP': None, 'SR': None, 'SS': None,
                         'SP': None, 'PR': None, 'PS': None, 'PP': None}

        self.distribution = {'RR': 0, 'RS': 0, 'RP': 0, 'SR': 0, 'SS': 0, 'SP': 0,
                             'PR': 0, 'PS': 0, 'PP': 0}

    def new_move(self, input):
        last_move = input[0:2]

        if len(input) > 2:
            if self.children[last_move] is None:
                self.children[last_move] = HistoryNode(self)
            self.children[last_move].new_move(input[2:])
        else:
            self.distribution[last_move] = self.distribution[last_move] * 0.975 + 1

    def predict(self, input):
        if len(input) > 0:
            last_move = input[0:2]
            if self.children[last_move] is not None:
                return self.children[last_move].predict(input[2:])
            else:
                return None
        else:
            return self.distribution


class HistoryTree(object):
    def __init__(self):
        self.root = HistoryNode()

        self.input = ''

    def new_move(self, move):
        self.input += move
        if len(self.input) > SIZE * 2:
            self.input = self.input[-SIZE * 2:]

        for i in xrange(2, len(self.input) + 1, 2):
            self.root.new_move(self.input[-i:])

    def predict(self):
        results = {'R':0, 'S':0, 'P':0}
        for i in xrange(2, len(self.input) + 1, 2):
            res = self.root.predict(self.input[-i:])
            #print "i",i,"res:",res
            if res is not None:
                for key in res:
                    #print "key[1]",key[1],"res[key]",res[key]
                    results[key[1]] += res[key] * (WEIGHT_FACTOR ** i)
                    print results[key[1]]

        d = results
        e = d.keys()
        e.sort(cmp=lambda a, b: cmp(d[a], d[b]))
        #print "results",results,"e",e
        return e[-1]
    
    def predict_i(self, i):
        results = {'R':0, 'S':0, 'P':0}
        for depth in xrange(i, -1, -1):
            res = self.root.predict(self.input[-depth * 2:])
            if res is not None:
                break
        
        if res is None:
            return random.choice(["R", "P", "S"])
        else:
            for key in res:
                results[key[1]] += res[key]
            
        d = results
        e = d.keys()
        e.sort(cmp=lambda a, b: cmp(d[a], d[b]))
        return e[-1]



class N(object):
    def __init__(self, parent=None):
        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        self.children = {'R': None, 'S': None, 'P': None}

        self.distribution = {'R':0, 'S':0, 'P':0}

    def new_move(self, input):
        #analyse last move
        last_move = input[0]

        if len(input) > 1:
            if self.children[last_move] is None:
                self.children[last_move] = HistoryNode(self)
            self.children[last_move].new_move(input[1:])
        else:
            self.distribution[last_move] += self.distribution[last_move] * 0.975 + 1

    def predict(self, input):
        if len(input) > 0:
            last_move = input[0]
            if self.children[last_move] is not None:
                return self.children[last_move].predict(input[1:])
            else:
                return None
        else:
            return self.distribution

    def __str__(self):
        if self.children['R'] != None:
            print self.children['R']
        if self.children['S'] != None:
            print self.children['S']
        if self.children['P'] != None:
            print self.children['P']
        return "profundidad "+str(self.depth)+" distribucion R:"+str(self.distribution['R'])+" S:"+str(self.distribution['S'])+" P:"+str(self.distribution['P'])
        

class HistoryTree(object):
    def __init__(self):
        self.root = HistoryNode()

        self.input = ''

    def new_move(self, input):
        self.input += input
        if len(self.input) > 10:
            self.input = self.input[-10:]

        for i in xrange(1,len(self.input)+1):
            self.root.new_move(self.input[-i:])

    def predict(self):
        results = {'R':0,'S':0,'P':0}
        for i in xrange(1, len(self.input)+1):
            res = self.root.predict(self.input[-i:])
            #print res
            if res is not None:
                for key in res:
                    results[key] += res[key] * (1.5**i)

        d = results
        print d
        e = d.keys()
        e.sort(cmp=lambda a,b: cmp(d[a],d[b]))
        return e[-1]

    def imprimir_arbol(self):
        print self.root
