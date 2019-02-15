"""
@author: Halit Uyanık
"""

import numpy as np
import sys
import random
import math

class Graph:
    def __init__(self, N, E):
        self.N = N
        self.E = E

        self.adj_list = []
        for i in range(self.N):
            self.adj_list.append([])

        self.color_list = np.zeros(len(self.adj_list), dtype=int)

    def add_edge(self, edge):
        # add edge to adjaceny list
        self.adj_list[edge[0]].append(edge[1])
        self.adj_list[edge[1]].append(edge[0])

def read_data(file_name):
    f = open(file_name)
    N, E = [int(el) for el in f.readline().rstrip().split(" ")]
    g = Graph(N, E)
    for line in f:
        edge = [int(el) for el in line.rstrip().split(" ")]
        g.add_edge(edge)
    return g

"""
MXRLF algorithm
Colors the most important vertices according to their future affects
on non-colored and the neighborhoods of colored other vertices.
"""
def MXRLF(graph):
    nIter = 50
    bestColoring = None
    bestK = graph.N
    vertices = np.arange(graph.N)

    np.random.seed(1773)

    while nIter != 0:
        nIter -= 1
        # Reset coloring
        graph.color_list = np.zeros(graph.N, dtype=int)

        color_class = 1
        MXRLF_LIMIT = int(0.7 * graph.N)
        while 0 in graph.color_list:
            vertex_list = [v for v in vertices if feasibleV(v, graph) != -1]
            init = np.random.choice(vertex_list, 1)[0]
            # Add the highest degree vertex to first color class
            graph.color_list[init] = color_class        
            while True:
                if len([i for i in graph.color_list if i == color_class]) > MXRLF_LIMIT:
                    break
                P = []
                for i in range(graph.N):
                    if graph.color_list[i] == 0 and not [adj for adj in graph.adj_list[i] if graph.color_list[adj] == color_class]:
                        P.append(i)
                if not P:
                    break
                R = []
                for i in range(graph.N):
                    if graph.color_list[i] == 0 and [adj for adj in graph.adj_list[i] if graph.color_list[adj] == color_class]:
                        R.append(i)        
                # Sort
                P = sorted(P, key=lambda x: (degreeInR(x, R, graph), degreeInP(x, P, graph)), reverse=True)
                # Change the color
                graph.color_list[P[0]] = color_class
            # Next color class
            color_class += 1
        
        if color_class - 1 < bestK:
            bestK = color_class - 1
            bestColoring = graph.color_list.copy()
    
    return bestK, bestColoring

# Checks if the vertex has proper coloring with its neighbors
def feasibleV(v, graph):
    if graph.color_list[v] != 0:
        return -1
    else:
        non_c_neig = 0
        for n in graph.adj_list[v]:
            if graph.color_list[n] == 0:
                non_c_neig += 1
        return non_c_neig
# Degree of a vertex in the set of colored vertices
def degreeInR(v, R, G):
    all_neig = G.adj_list[v]
    intersection = list(set(all_neig).intersection(set(R)))
    return len(intersection)
# Degree of a vertex in the set of non-colored vertices
def degreeInP(v, P, G):
    all_neig = G.adj_list[v]
    intersection = list(set(all_neig).intersection(set(P)))
    return 1.0/(len(intersection)+1e-10)

if __name__ == "__main__":
    g = read_data(sys.argv[1])

    count, color_list = MXRLF(g)

    print(count)
    for c_l in color_list:
        print('%d ' % c_l, end='')