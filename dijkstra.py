 # modified version of python implementation of Dijkstra's Shortest
 #Path Algorithm by Asanka P. Sayakkara. Original code can be found at
# http://recolog.blogspot.com/2012/02/dijkstras-shortest-path-algorithm.html
 
  #!/usr/bin/python  
import string  
import time  

from dict_to_tnodes import * 
        
def main():
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth = opts.depth

    sTime = time.time()
	
    output_f = open("output.txt", "w+")
    
    print "Crawling %s (Max Depth: %d)" % (url, depth)
    crawler = Crawler(url, depth)
    crawler.crawl()
    dict = crawler.urls
    #create ring of one-node circnodes with the urls found
    fibheap = from_dict_to_fibheap(dict, url)
    
    
    
  # represents a vertex in the graph  
class Vertex:  
       def __init__(self, name):  
            self.name = name         # name of the vertex  
            self.dist = 1000         # distance to this vertex from start vertex  
            self.prev = None        # previous vertex to this vertex  
            self.flag = 0           # access flag  
     
     
  # represents an edge in the graph  
class Edge:  
       def __init__(self, u, v, length):  
            self.start = u  
            self.end = v  
            self.length = length  
    
    
# read a text file and generate the graph according to declarations  
def generateGraph(V, E):  
       file = open("graph_def", "r")  
       line = file.readline()  
       line = line[:-1]  
       while line:  
            taglist = string.split(line)  
            if taglist[0] == 'vertex':  
                 V.append(Vertex(taglist[1]))  
            elif taglist[0] == 'edge':  
                 E.append(Edge(taglist[1], taglist[2], string.atoi(taglist[3])))  
                 E.append(Edge(taglist[2], taglist[1], string.atoi(taglist[3])))  
            line = file.readline()  
            line = line[:-1]            
       file.close()  
    
    
  # returns the smallest vertex in V but not in S  
def pickSmallestVertex(V):  
       minVertex = None  
       for vertex in V:  
            if vertex.flag == 0:  
                 minVertex = vertex  
                 break  
       if minVertex == None:  
            return minVertex  
       for vertex in V:  
            if vertex.flag == 0 and vertex.dist < minVertex.dist:  
                 minVertex = vertex  
       return minVertex  
    
    
  # returns the edges list of vertex u  
def pickEdgesList(u, E):  
       uv = []  
       for edge in E:  
            if edge.start == u.name:  
                 uv.append(edge)  
       return uv  
    
    
def findShortestPath(V, E, S, A):  
       # set A vertex distance to zero  
       for vertex in V:  
            if vertex.name == A:  
                 vertex.dist = 0  
    
       u = pickSmallestVertex(V)  
       while u != None:  
            u.flag = 1  
            uv = pickEdgesList(u, E)  
            v = None  
            for edge in uv:  
                 # take the vertex v  
                 for vertex in V:  
                      if vertex.name == edge.end:  
                           v = vertex  
                           break  
                 if v.dist > u.dist + edge.length:  
                       v.dist = u.dist + edge.length  
                       v.prev = u  
            u = pickSmallestVertex(V)  
    
    
def printGraph(V, E):  
       print('vertices:')  
       for vertex in V:  
            previous = vertex.prev       
            if previous == None:  
                 print(vertex.name, vertex.dist, previous)  
            else:  
                 print(vertex.name, vertex.dist, previous.name)  
       print('edges:')  
       for edge in E:       
            print(edge.start, edge.end, edge.length)  
    
    
def main():  
       print('Starting Dijkstra\'s Algorithm...')       
       t1 = time.time()  
       # graph elements  
       V = []  
       E = []  
       S = []  
       generateGraph(V, E)       
       printGraph(V, E)  
       findShortestPath(V, E, S, 'a')  
       printGraph(V, E)  
       print 'dummy '         
       t2 = time.time()  
       print t2-t1  
    
    
main()  