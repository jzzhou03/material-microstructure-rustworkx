This is testing of graph capabilites of RustworkX for Material Microstructures.

To be able to create and visualize graphs, you'll need to run these following commands in your terminal:  
  
&emsp; INSTALLING RUSTWORKX (x86_64, i686, ppc64le, s390x, aarch64 Linux systems, and x86_64, arm64 macOS, and 32, 64 bit Windows):  
  &emsp; &emsp; `pip install rustworkx`  
  
&emsp; VISUALIZATION:  
  &emsp; &emsp; Graphviz (Differs from systems):  
    &emsp; &emsp; &emsp; https://graphviz.org/download/#executable-packages  
  &emsp; &emsp; Pydot (Required with Graphviz):  
    &emsp; &emsp; &emsp; `pip install pydot pillow`  
     &emsp; &emsp; MatPlotLib:  
  &emsp; &emsp; &emsp; `pip install matplotlib`
  
CODE STRUCTURE:  
  
Global Variables:  
  &emsp; graph  
    &emsp; &emsp; - using the PyGraph class provided by rustworkx, nodes will be added to this variable in order to visualize a graph.  
  &emsp; filteredGraph  
    &emsp; &emsp; - created to store the filtered original "graph" and be able to call it later on when looking for shortest paths.  

Classes:  
  &emsp; Node  
    &emsp; &emsp; Custom class that stores node data:  
      &emsp; &emsp; &emsp; - Label (node number/indice)  
      &emsp; &emsp; &emsp; - Color  
      &emsp; &emsp; &emsp; - X coordinate  
      &emsp; &emsp; &emsp; - Y coordinate  
      &emsp; &emsp; &emsp; - Z coordinate  
  &emsp; Edge  
    &emsp; &emsp; Custom class that stores edge data:  
      &emsp; &emsp; &emsp; - From node  
      &emsp; &emsp; &emsp; - To node  
      &emsp; &emsp; &emsp; - Weight  

Functions  
  &emsp; createGraph(filename):  
    &emsp; &emsp; - Takes in a string file name as a parameter which is used to read a file and graphs the nodes depending on the format of the file.  
    &emsp; &emsp; - Currently only allows for structured data  
    &emsp; &emsp; - Adds a node and edges between it and all its possible neighbors.  

 &emsp;  add_cathode_node(dimX, dimY, dimZ):  
    &emsp; &emsp; - takes in dimension parameters given in file which should have already been initialized in the createGraph() function.  
    &emsp; &emsp; - called at end of createGraph to add cathode node and connects it to bottom black layer.  
    
  &emsp; node_attr_fn(node):  
    &emsp; &emsp; - Takes in a node class as a parameter  
    &emsp; &emsp; - Makes a dictionary that adds attributes onto the nodes for graph visualization.  
    &emsp; &emsp; - Class is used as a parameter when visualizing graph using graphViz format.  

 &emsp;  visualizeGraphMPL(g):  
    &emsp; &emsp; - Takes in a graph g  
    &emsp; &emsp; - Visualizes the graph using mpl_draw function given by the rustworkx package and matplotlib package  

  &emsp; visualizeGraphGV(g, file):  
    &emsp; &emsp; - Takes in a graph g and a filename to store the filtered graph visualization.  
    &emsp; &emsp; - Visualizes graph using the graphviz_draw() format.  
    &emsp; &emsp; - Recommended by rustworkx documentation for graphs with a lot of nodes.  

  &emsp; testGraphRuntime(filename, visualize, times):  
    &emsp; &emsp; - Takes in a string filename, a boolean variable visualize that states if user wants a visual of graph, and an int variable of how many times it wishes the program to run.  
    &emsp; &emsp; - It also returns an average of how long it took for the program to run each time.  

  &emsp; filterGraph(visualize):  
    &emsp; &emsp; - Filtering function that takes in the variable that allows for visualization or no visualization  
    &emsp; &emsp; - Returns list of edges that meet the filter  

  &emsp; connectedComponents(edge):  
    &emsp; &emsp; - Function used to filter edges by node color  
    &emsp; &emsp; - Required for built in graph filtering  

  &emsp; def filterGraph(g, visualize):  
    &emsp; &emsp; - Takes in a graph and a boolean that states if filtered graph should be visualized	 
    &emsp; &emsp; - Uses connected components to get desired filtered edge list.which we use to make a tuple of nodes.  
    &emsp; &emsp; - Uses this list of node tuples to create filtered graph with rustworkx built in function edge_subgraph().  
  
 &emsp;  def testFilterGraph(g, filename, visualize, times):  
    &emsp; &emsp; - Takes in a graph, string filename, a boolean variable visualize that states if the user wants a visual of the graph after filtering, and an int variable times of how many times the user wishes the program to run  
    &emsp; &emsp; - It also returns an average of how long it took for the program to run each time  

  &emsp; def dfs_search(g, source):  
    &emsp; &emsp; - Takes in graph as well as a source node to start a dfs search.  
    &emsp; &emsp; - Outputs a list of all connected nodes found from source node while running dfs.  

  &emsp; def bfs_search(g, source):  
    &emsp; &emsp; - Takes in graph as well as a source node to start a bfssearch.  
    &emsp; &emsp; - Outputs a list of all connected nodes found from source node while running bfs.  

  &emsp; def shortest_path(g):  
    &emsp; &emsp; - Takes in a graph  
    &emsp; &emsp; - Finds the shortest path to all black nodes from the cathode  
    &emsp; &emsp; - Returns a dictonary of paths to each possible node  
