
import networkx as nx

class BnetGraph(nx.DiGraph):
    def add_nodes_from(self, nodes):
        for n in nodes:
            n.graph = self
        nx.DiGraph.add_nodes_from(self, ((n.variables(),{'factor':n}) for n in nodes))
