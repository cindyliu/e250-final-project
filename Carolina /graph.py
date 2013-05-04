#Library to format graph data into JSON format
from networkx.readwrite import json_graph

#Library to export graph data to JSON format file
import json

#Library to create graph 
import networkx as nx

#Code to run a simple Python server to display results
import http_server


# takes a dict makes a networkx graph
def dict_2_graph(dict,home_url) :

 #Creating a graph of the dict for plotting
    G=nx.Graph()
    
    #first key is going to be the start url 
    
    for key in dict:
        G.add_node(key.lower())
         
        for val_url in dict[key]:
            G.add_edge(key.lower(),val_url.lower(),type="fib")
         
    G.add_node(home_url.lower(),type="home")
         
    return G