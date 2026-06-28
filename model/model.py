from random import randint

import networkx as nx
from geopy.distance import great_circle
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._bestPath = []

    # -- PATH SEARCHING --

    def findBestPath(self, end, s):
        self._bestPath = []
        nodi_start = self.getMoreVicini()[0]

        if s in end:
            return self._bestPath

        while True:
            nodo_scleto = nodi_start[randint(0, len(nodi_start) - 1)]
            if s not in nodo_scleto:
                break


        parziale = [nodo_scleto]
        self._ricorsione(parziale, end, s)

        return self._bestPath

    def _ricorsione(self, parziale, end, s):
        nodo_corrente = parziale[-1]

        if nodo_corrente == end:
            if len(parziale) > len(self._bestPath):
                self._bestPath = parziale.copy()
            # SE è GIA STATO AGGIUNTO END E NON E MIGLIORE è
            # INUTILE CONTINUARE A ESPLORARE QUEL RAMO
            return

        for n in self._graph.neighbors(nodo_corrente):
            if s in n:
                continue

            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, end, s)
                parziale.pop()

    # -- BUILD GRAPH --

    def buildGraph(self, d, provider):
        self._graph.clear()
        self._buildNodes(provider)
        self._buildEdges(d, provider)

    def _buildNodes(self, provider):
        locations = DAO.getLocalitaByProvider(provider)
        self._graph.add_nodes_from(locations)

    def _buildEdges(self, d, provider):
        locations_data = DAO.getCorrelazioni(provider)
        correlazioni = []
        l_keys = list(locations_data.keys())
        for i in range(len(l_keys)):
            for j in range(i+1, len(l_keys)):
                l1 = l_keys[i]
                l2 = l_keys[j]
                distance_km = great_circle(locations_data[l1], locations_data[l2]).km
                if distance_km <= d:
                    correlazioni.append((l1, l2, distance_km))

        self._graph.add_weighted_edges_from(correlazioni)

    @staticmethod
    def getAllProviders():
        return DAO.getAllProviders()

    def getInfoGraph(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getMoreVicini(self):
        best = 0
        for n in self._graph.nodes:
            n_vicni = len(list(self._graph.neighbors(n)))
            if n_vicni > best:
                best = n_vicni
        bestlist = []
        for n in self._graph.nodes:
            if len(list(self._graph.neighbors(n))) == best:
                bestlist.append(n)

        return bestlist, best

    def getAllNodes(self):
        return list(self._graph.nodes)

