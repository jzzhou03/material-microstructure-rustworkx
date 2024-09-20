import rustworkx as rx
import math
import graphviz
import matplotlib.pyplot as plt
import time

from rustworkx import *
from rustworkx.visit import *
from rustworkx.visualization import *

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

file2 = "tests/2x2.txt"
file3 = "tests/3x4.txt"

file10 = "tests/10x10.txt"
file50 = "tests/50x50.txt"
file100 = "tests/100x100.txt"
file500 = "tests/500x500.txt"
file1000 = "tests/1000x1000.txt"

file3D10 = "tests/10x10x10.txt"
file3D50 = "tests/50x50x50.txt"
file3D100 = "tests/100x100x100.txt"

class Node:
   def __init__(self, label, color, x, y, z):
       self.label = label
       # Color of the node depending on 0 or 1
       self.color = color
       # Coordinates of the node
       self.x = x
       self.y = y
       self.z = z

class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

class TreeEdgesRecorderDfs(DFSVisitor):

    def __init__(self):
        self.edges = []

    def tree_edge(self, edge):
        self.edges.append(edge)

class TreeEdgesRecorderBfs(BFSVisitor):

    def __init__(self):
        self.edges = []

    def tree_edge(self, edge):
        self.edges.append(edge)


graph = rx.PyGraph()
filteredGraph = rx.PyGraph()

def createGraph(filename, cathode):
    with open(filename, "r") as f:
        lines = f.readlines()
        header = lines[0].split()

        # Dimensions of the graph
        dimX, dimY, dimZ = map(int, header)

        # Stores necessary data for creating edges
        prevLayer = [[None] * dimX for i in range(dimY)]
        currLayer = [[None] * dimX for i in range(dimY)]
        prevRow = [None] * dimX  # Allocates necessary space beforehand
        currRow = [None] * dimX  # Allocates necessary space beforehand
        prevNode = None

        line_idx = 1

        # Graph creation
        for z in range(dimZ):
            for y in range(dimY):
                line = lines[line_idx].strip().split(" ")
                line_idx += 1
                for x in range(dimX):
                    node = graph.add_node(Node((z * dimX * dimY) + (y * dimX) + x, int(line[x]), x, y, z))
                    currRow[x] = node
                    currLayer[y][x] = node

                    # Left of the node
                    if prevNode != None:
                        graph.add_edge(node, prevNode, Edge(node, prevNode, 1))

                    # Down of the node
                    if prevRow[x] != None:
                        graph.add_edge(node, prevRow[x], Edge(node, prevRow[x], 1))

                    if (prevLayer[y][x] != None):
                        graph.add_edge(node, prevLayer[y][x], Edge(node, prevLayer[y][x], 1))

                    # Southeast of the node
                    if (x + 1 < dimX) and (prevRow[x + 1] != None):
                        graph.add_edge(node, prevRow[x + 1], Edge(node, prevRow[x + 1], math.sqrt(2)))

                    # Southwest of the node
                    if (x - 1 >= 0) and (prevRow[x - 1] != None):
                        graph.add_edge(node, prevRow[x - 1], Edge(node, prevRow[x - 1], math.sqrt(2)))

                    # Checks if the node isn't the last node on the line
                    if (x < dimX - 1):
                        prevNode = node
                    else:
                        prevNode = None
                # Stores the previous row as the current row, clears current row
                prevRow, currRow = currRow, [None] * dimX

            prevLayer, currLayer = currLayer, [[None] * dimX for i in range(dimY)]
        if (cathode):
            add_cathode_node(dimX, dimY, dimZ)

def add_cathode_node(dimX,dimY,dimZ):
    cathode = graph.add_node(Node("Interface", 2, 0, 0, 0))
    currNodes = graph.node_indices()
    for z in range(dimZ):
        for x in range(dimX):
            graph.add_edge(cathode, currNodes[z * dimX + x], Edge(cathode, currNodes[z * dimX + x], 1))


def visualizeGraphMPL(g):
    rx.visualization.mpl_draw(g)
    plt.show()

def node_attr_fn(node):
    attr_dict = {
      "style": "filled",
      "shape": "circle",
      "label": str(node.label),
      "rank": "same"
    }
  #find out how to reach into Node class for color
  #if node is 0 make black, if 1 make white
    if node.color == 2:
        attr_dict["color"] = "black"
        attr_dict["fillcolor"] = "green"
    elif node.color == 1:
        attr_dict["color"] = "black"
        attr_dict["fillcolor"] = "black"
        attr_dict["fontcolor"] = "white"
    else:
        attr_dict["color"] = "black"
        attr_dict["fillcolor"] = "white"
    return attr_dict

def visualizeGraphGV(g, file):
    # for node in graph.node_indices():
        # graph[node] = graph.get_node_data(node)
    graph_dict = {}
    graphviz_draw(g, filename=file, node_attr_fn=node_attr_fn, graph_attr=graph_dict, method ="neato")

def testGraphRunTime(filename, visualize, cathode, times):
    totalTime = 0;
    if visualize:
        for i in range(times):
            start = time.time()
            createGraph(filename, cathode)
            visualizeGraphGV(graph, "images/rustworkx_graph.jpg")
            totalTime += time.time() - start
    else:
        for i in range(times):
            start = time.time()
            createGraph(filename, cathode)
            totalTime += time.time() - start
    print(totalTime/times)
    return (totalTime / times)

def connectedComponents(edge):
    node1 = graph.get_node_data(edge.node1)
    node2 = graph.get_node_data(edge.node2)

    # Checks if the edge between the two nodes have different colors
    if ( (node1.color == 0 and node2.color == 1) or (node1.color == 1 and node2.color == 0) ):
        return False
    return True

def filterGraph(g, visualize):
    global filteredGraph
    edges = g.filter_edges(connectedComponents)
    edgeList = []

    for edge in edges:
        node1 = g.get_edge_data_by_index(edge).node1
        node2 = g.get_edge_data_by_index(edge).node2
        edgeList.append( (node1, node2) )

    filteredGraph = g.edge_subgraph(edgeList)

    if visualize:
        visualizeGraphGV(filteredGraph, "images/rustworkx_subgraph.jpg")

    return edges

def testFilterGraph(filename, visualize, cathode, times):
    totalTime = 0
    for i in range(times):
        start = time.time()
        createGraph(filename, cathode)
        filterGraph(graph, visualize)
        totalTime += time.time() - start
    print(totalTime / times)
    return (totalTime / times)

#Uses DFS to traverse graph and print's all edges reachele from source node
def dfs_search(g, source):
    nodes = []
    nodes.append(source)
    visDFS = TreeEdgesRecorderDfs()
    rx.dfs_search(g, nodes, visDFS)
    print('DFS Edges:', visDFS.edges)

#Uses BFS to traverse graph and print's all edges reachele from source node
def bfs_search(g, source):
    nodes = []
    nodes.append(source)
    visBFS = TreeEdgesRecorderBfs()
    rx.bfs_search(g, nodes, visBFS)
    print('BFS Edges:', visBFS.edges)

#finds shortest path between a source and target node
def shortest_path(g):
    cathode = g.num_nodes() - 1
    all_paths = dijkstra_shortest_paths(g, cathode)
    return [all_paths[node] for node in all_paths.keys() if g.get_node_data(node).color == 1]

# Used for creating CSV files for data of testing
"""
import tracemalloc
import csv

def functionRuntime(count, function, *argv):
    totaltime = 0

    for x in range(count):
        startTime = time.time()
        function(*argv)
        endTime = time.time()
        timeTaken = endTime - startTime
        totaltime += timeTaken

    avgExecution = totaltime / count

    return avgExecution


def functionMemory(function, *argv):
    tracemalloc.start()
    function(*argv)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    stats = stats[1] - stats[0]

    return stats

def csvMaker(fileName, n, dim, count, graphGen, graphGenPar, graphFilt, graphFiltPar, shortPath, shortPathPar):
    row = [n, (n ** dim)]
    totalTime = 0
    totalMem = 0

    graphGenRuntime = functionRuntime(count, graphGen, *graphGenPar)
    graphFiltRuntime = functionRuntime(count, graphFilt, *graphFiltPar)
    shortPathRuntime = functionRuntime(count, shortPath, *shortPathPar)

    totalTime = graphGenRuntime + graphFiltRuntime + shortPathRuntime
    totalTime = round(totalTime, 20)

    graphGenMem = functionMemory(graphGen, *graphGenPar)
    graphFiltMem = functionMemory(graphFilt, *graphFiltPar)
    shortPathMem = functionMemory(shortPath, *shortPathPar)

    totalMem = graphGenMem + graphFiltMem + shortPathMem
    totalMem = round(totalMem, 20)

    row.append(graphGenRuntime)
    row.append(graphFiltRuntime)
    row.append(shortPathRuntime)
    row.append(totalTime)
    row.append(totalMem)

    with open(fileName, 'a', newline="\n") as file:
        writer = csv.writer(file)
        writer.writerow(row)


fileName = "tests/10x10.txt"
createGraph(fileName, False)
filterGraph(graph, False)

csvMaker("RustworkX_Test_Results.csv", 10, 2, 3, createGraph, [fileName], filterGraph, [graph, False],
         shortest_path, [filteredGraph])

fileName = "tests/50x50.txt"
createGraph(fileName, False)
filterGraph(graph, True)

csvMaker("RustworkX_Test_Results.csv", 50, 2, 3, createGraph, [fileName], filterGraph, [graph, False],
         shortest_path, [filteredGraph])

fileName = "tests/100x100.txt"
createGraph(fileName, False)
filterGraph(graph, False)

csvMaker("RustworkX_Test_Results.csv", 100, 2, 3, createGraph, [fileName], filterGraph, [graph, False],
         shortest_path, [filteredGraph])

fileName = "tests/500x500.txt"
createGraph(fileName, False)
filterGraph(graph, False)

csvMaker("RustworkX_Test_Results.csv", 500, 2, 3, createGraph, [fileName], filterGraph, [graph, False],
         shortest_path, [filteredGraph])

fileName = "tests/1000x1000.txt"
createGraph(fileName, False)
filterGraph(graph, False)

csvMaker("RustworkX_Test_Results.csv", 1000, 2, 3, createGraph, [fileName], filterGraph, [graph, False],
         shortest_path, [filteredGraph])
"""