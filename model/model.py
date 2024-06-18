import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGraph(self, durata):
        self._album = DAO.getAlbums(durata)
        self._grafo.add_nodes_from(self._album)

        for a in list(self._grafo.nodes):
            self._idMap[a.AlbumId] = a

        edges = DAO.getEdges(self._idMap) #lista di tuple
        self._grafo.add_edges_from(edges)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getNodes(self):
        return list(self._grafo.nodes)

    def getConnessaDetails(self, v0):
        self._bestSet = None
        self._bestScore = 0

        connessa = nx.node_connected_component(self._grafo, v0)
        totDurata = 0

        for album in connessa:
            totDurata += album.totD

        return len(connessa), toMinutes(totDurata)

    def getSetAlbum(self, a1, dTot):
        connessa = nx.node_connected_component(self._grafo, a1)
        parziale = set([a1])
        connessa.remove(a1)

        self.ricorsione(parziale, connessa, dTot)

        return self._bestSet


    def ricorsione(self, parziale, connessa, dTot):
        #Verificare se parziale è una soluzione ammissibile
        if self.durataTot(parziale) > dTot:
            return

        # Verificare se parziale è migliore di best
        if len(parziale) > self._bestScore:
            self._bestScore = len(parziale)
            self._bestSet = copy.deepcopy(parziale)

        #Aggiungo un altro album al set --> ricorsione
        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                rimanenti = copy.deepcopy(connessa)
                rimanenti.remove(c)
                self.ricorsione(parziale, rimanenti, dTot)
                parziale.remove(c)

    def durataTot(self, setOfNodes):
        durata = 0
        for node in setOfNodes:
            durata += node.totD
        return toMinutes(durata)


    def getNodesI(self, i):
        return self._idMap[self._grafo.nodes[261]]

def toMillisec(durata):
    return durata * 1000 * 60

def toMinutes(durata):
    return durata/(1000 * 60)