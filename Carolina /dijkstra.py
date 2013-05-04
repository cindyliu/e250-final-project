#!/usr/bin/python  
from dict_to_tnodes import * 
       
#algorithm to find the shortest path from the home page 
#(min node of the heap) to the destination url
#takes in the fibheap generated from the starting link
#and the url of the desired destination

def findShortestPath(fibheap,destination,output_f,G): 
    dij_path = []
    dij_path.append(fibheap.min.tree.root.self_url)
    print ("Starting shortest path...")
    finished = False
    #print (fibheap.is_empty(output_f))
    while not fibheap.is_empty(output_f):
        # set current node
        current = fibheap.min.tree.root
        #print "\nthis is url of fibheap min " + (fibheap.min.tree.root.self_url) 
        #print "this is key/dist of fibheap min " + repr(fibheap.min.tree.root.key)
        #print "fibheap 'size' is: " + repr(fibheap.size)      
        #print "fibheap 'total_size' is: " + repr(fibheap.total_size)            
        #print "number of children of min is: " + repr(len(fibheap.min.tree.root.children))
        if current.self_url == destination.lower():
                print "Shortest path from starting url to destination URL is " + repr(current.key) + " steps"
                # print out shortest path back to starting url 
                current_tnode_printed = current
                while current_tnode_printed.dij_prev != None:
                    #print current_tnode_printed.self_url
                    #Updating type and dist fields of nodes in graph to indicate it is part of the shortest path
                    #P=G.node[current_tnode_printed.self_url]["path"]
                    #P.add_edge(current_tnode_printed.self_url,current_tnode_printed.dij_prev.self_url,type="dij")
                    G[current_tnode_printed.self_url][current_tnode_printed.dij_prev.self_url]["type"]="dij"
                    G.add_node(current_tnode_printed.self_url,type="dij",dist=current_tnode_printed.key) 
                    dij_path.append(current_tnode_printed.self_url)   
                    current_tnode_printed = current_tnode_printed.dij_prev
                print current_tnode_printed.self_url 
                #finished = True 
                break
        
       #updating distances of neighbors, if necessary  	
        #print current.self_url    
        for neighbor in current.neighbors:
            #print ('Iterating through neighbors') #print str(neighbor.key) + " " + str(current.key +1)
            if (not neighbor.finished) and (neighbor.key > (current.key +1)):
                #print ("Updating Dists...")  
                fibheap.decr_key(neighbor,current.key +1,output_f)
                neighbor.dij_prev = current
                #Updating dist field in graph nodes
                G.add_node(current.self_url,dist=current.key)  
                
        #after checking all neighbors and updating as necessary, this node is in "finished" pile
        current.finished = True
        
        #if (not finished):
    	G.add_node(current.self_url,status="finished",dist=current.key)
    	if current.dij_prev != None:
           	G[current.self_url][current.dij_prev.self_url]["type"]="finished"
       	    	
       	       
        
        
        fibheap.pop(output_f)
    return G, dij_path