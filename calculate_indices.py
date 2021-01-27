import networkx
from networkx import algorithms
from networkx.algorithms import isomorphism
import networkx as nx

def calculate_wiener(G):
    return nx.average_shortest_path_length(G, weight='weight')* len(G)*(len(G)-1) * 0.5

def calcuate_pisanski(G):
    GM = algorithms.isomorphism.GraphMatcher(G, G)
    paths_len = 0
    for isomorph in GM.isomorphisms_iter():
        for v1, v2 in isomorph.items():
            paths_len += algorithms.shortest_path_length(G, v1, v2)
    return((paths_len*len(G))/(len(list(GM.isomorphisms_iter())) * 2))
