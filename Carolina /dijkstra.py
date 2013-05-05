#!/usr/bin/python  
from dict_to_tnodes import *
from operator import attrgetter
 
#algorithm to find the shortest path from the home page 
#(min node of the heap) to the destination url
#takes in the priority queue generated from the starting link
#and the url of the desired destination

def findShortestPath_PQ(prioq,destination,G):
    dij_path = []
    dij_path.append(prioq.queue[0].self_url) 
    print ("Starting shortest path...")
    print (prioq.empty())
    while not prioq.empty() :
        # set current node
        current = prioq.queue[0]
        if current.self_url == destination.lower():
                print "Shortest path from starting url to destination url is " + repr(current.key) + " steps"
                # print out shortest path back to starting url 
                current_tnode_printed = current
                while current_tnode_printed.dij_prev != None:
                    print current_tnode_printed.self_url
                    G[current_tnode_printed.self_url][current_tnode_printed.dij_prev.self_url]["type"]="dij"
                    G.add_node(current_tnode_printed.self_url,type="dij",dist=current_tnode_printed.key) 
                    dij_path.append(current_tnode_printed.self_url)   
                    current_tnode_printed = current_tnode_printed.dij_prev
                print current_tnode_printed.self_url  
                break

        #updating distances of neighbors, if necessary       		      
        for neighbor in current.neighbors:
            if (not neighbor.finished) and (neighbor.key > (current.key + 1)):
                neighbor.key = current.key + 1
                prioq.queue.sort(key=attrgetter("key"))
                neighbor.dij_prev = current
                G.add_node(current.self_url,dist=current.key)  
                
        #after updating as necessary, this node is in "finished" pile
        current.finished = True
        
        
    	G.add_node(current.self_url,status="finished",dist=current.key)
    	if current.dij_prev != None:
            G[current.self_url][current.dij_prev.self_url]["type"]="finished"
       	    	
        
        pq_pop(prioq)
        
    return G, dij_path
    
    
def findShortestPath(fibheap,destination,output_f,G): 
    dij_path = []
    dij_path.append(fibheap.min.tree.root.self_url)
    print ("Starting shortest path...")
    while not fibheap.is_empty(output_f):
        # set current node
        current = fibheap.min.tree.root
        if current.self_url == destination.lower():
                print "Shortest path from starting url to destination URL is " + repr(current.key) + " steps"
                # print out shortest path back to starting url 
                current_tnode_printed = current
                while current_tnode_printed.dij_prev != None:
                    G[current_tnode_printed.self_url][current_tnode_printed.dij_prev.self_url]["type"]="dij"
                    G.add_node(current_tnode_printed.self_url,type="dij",dist=current_tnode_printed.key) 
                    dij_path.append(current_tnode_printed.self_url)   
                    current_tnode_printed = current_tnode_printed.dij_prev
                print current_tnode_printed.self_url  
                break
        
       #updating distances of neighbors, if necessary  	  
        for neighbor in current.neighbors:
            if (not neighbor.finished) and (neighbor.key > (current.key +1)):  
                fibheap.decr_key(neighbor,current.key +1,output_f)
                neighbor.dij_prev = current
                #Updating dist field in graph nodes
                G.add_node(current.self_url,dist=current.key)  
                
        #after checking all neighbors and updating as necessary, this node is in "finished" pile
        current.finished = True
        
    	G.add_node(current.self_url,status="finished",dist=current.key)
    	if current.dij_prev != None:
           	G[current.self_url][current.dij_prev.self_url]["type"]="finished"
       	    	
       	     
        fibheap.pop(output_f)
    return G, dij_path
