This is testing of graph capabilites of RustworkX for Material Microstructures.

To be able to create and visualize graphs, you'll need to run these following commands in your terminal:  
  
INSTALLING RUSTWORKX (x86_64, i686, ppc64le, s390x, aarch64 Linux systems, and x86_64, arm64 macOS, and 32, 64 bit Windows):  
  pip install rustworkx  
  
GRAPHVIZ VISUALIZATION:  
  Graphviz:  
    https://graphviz.org/download/#executable-packages  
  Pydot:  
    pip install pydot pillow  
  
CODE STRUCTURE:  
  
Global Variables:  
  graph  
    - using the PyGraph class provided by rustworkx, nodes will be added to this variable in order to visualize a graph.  
  filteredGraph  
    - created to store the filtered original "graph" and be able to call it later on when looking for shortest paths.  

Classes:  
  Node  
    Custom class that stores node data:  
      - Label (node number/indice)  
      - Color  
      - X coordinate  
      - Y coordinate  
      - Z coordinate  
  Edge  
    Custom class that stores edge data:  
      - From node  
      - To node  
      - Weight  

Functions  
  createGraph(filename):  
    - Takes in a string file name as a parameter which is used to read a file and graphs the nodes depending on the format of the file.  
    - Currently only allows for structured data  
    - Adds a node and edges between it and all its possible neighbors.  

  add_cathode_node(dimX, dimY, dimZ):  
    - takes in dimension parameters given in file which should have already been initialized in the createGraph() function.  
    - called at end of createGraph to add cathode node and connects it to bottom black layer.  
    
  node_attr_fn(node):  
    - Takes in a node class as a parameter  
    - Makes a dictionary that adds attributes onto the nodes for graph visualization.  
    - Class is used as a parameter when visualizing graph using graphViz format.  

  visualizeGraphMPL(g):  
    - Takes in a graph g  
    - Visualizes the graph using mpl_draw function given by the rustworkx package and matplotlib package  

  visualizeGraphGV(g, file):  
    - Takes in a graph g and a filename to store the filtered graph visualization.  
    - Visualizes graph using the graphviz_draw() format.  
    - Recommended by rustworkx documentation for graphs with a lot of nodes.  

  testGraphRuntime(filename, visualize, times):  
    - Takes in a string filename, a boolean variable visualize that states if user wants a visual of graph, and an int variable of how many times it wishes the program to run.  
    - It also returns an average of how long it took for the program to run each time.  

  filterGraph(visualize):  
    - Filtering function that takes in the variable that allows for visualization or no visualization  
    - Returns list of edges that meet the filter  

  connectedComponents(edge):  
    - Function used to filter edges by node color  
    - Required for built in graph filtering  

  def filterGraph(g, visualize):  
    - Takes in a graph and a boolean that states if filtered graph should be visualized	 
    - Uses connected components to get desired filtered edge list.which we use to make a tuple of nodes.  
    - Uses this list of node tuples to create filtered graph with rustworkx built in function edge_subgraph().  
  
  def testFilterGraph(g, filename, visualize, times):  
    - Takes in a graph, string filename, a boolean variable visualize that states if the user wants a visual of the graph after filtering, and an int variable times of how many times the user wishes the program to run  
    - It also returns an average of how long it took for the program to run each time  

  def dfs_search(g, source):  
    - Takes in graph as well as a source node to start a dfs search.  
    - Outputs a list of all connected nodes found from source node while running dfs.  

  def bfs_search(g, source):  
    - Takes in graph as well as a source node to start a bfssearch.  
    - Outputs a list of all connected nodes found from source node while running bfs.  

  def shortest_path(g):  
    - Takes in a graph  
    - Finds the shortest path to all black nodes from the cathode  
    - Returns a dictonary of paths to each possible node  
