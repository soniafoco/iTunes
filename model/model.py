import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGrafo(self, durata):
        self._grafo.clear()

        self._albums = DAO.getAlbums()
        for album in self._albums:
            if album.Duration > durata*1000*60:
                self._grafo.add_node(album)
                self._idMap[album.AlbumId] = album

        self._albumPlaylist = DAO.getAlbumPlaylist(self._idMap)
        self._grafo.add_edges_from(self._albumPlaylist)

        print(self._grafo)

    def getDettagli(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getNodes(self):
        return list(self._grafo.nodes)


    def getConnessa(self, album):
        self._connessa = list(nx.node_connected_component(self._grafo, album))

        somma = 0
        for c in self._connessa:
            somma += c.Duration
        return len(self._connessa), somma/(60*1000)


    def getSetAlbum(self, soglia, album):

        self._bestSol = []
        self._bestScore = 0

        parziale = [album]
        for node in nx.neighbors(self._grafo, album):
            if node in self._connessa:
                parziale.append(node)
                self._ricorsione(parziale, soglia)
                parziale.pop()

        return self._bestSol, self._bestScore


    def _ricorsione(self, parziale, soglia):

        if self._getScore(parziale)<=soglia:
            if len(parziale)>self._bestScore:
                self._bestScore = len(parziale)
                self._bestSol = parziale[:]
        else:
            return

        for node in nx.neighbors(self._grafo, parziale[-1]):
            if node in self._connessa and node not in parziale:
                parziale.append(node)
                self._ricorsione(parziale, soglia)
                parziale.pop()

    def _getScore(self, list):
        somma = 0
        for node in list:
            somma += node.Duration
        return somma/(1000*60)