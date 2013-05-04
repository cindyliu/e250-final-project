#!/usr/bin/python  
from dict_to_tnodes_prioqueue_wiki import * 
from operator import attrgetter

#algorithm to find the shortest path from the home page 
#(min node of the heap) to the destination url
#takes in the priority queue generated from the starting link
#and the url of the desired destination

def findShortestPath_PQ(prioq,destination,G):
    dij_path = []
    dij_path.append(prioq.queue[0].self_url) 
    print ("Starting shortest path...")
    #finished = False
    print (prioq.empty())
    while not prioq.empty() :
        # set current node
        current = prioq.queue[0]
        print "this is url of prioqueue min: " + (current.self_url) 
        print "\t  key/dist: " + repr(current.key)
#        print "\t#neighbors: %d" % len(current.neighbors)
#        print "\t   ADDRESS: %d" % id(current)
#        print "prioqueue total size is: " + repr(prioq.qsize())
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
#        print "updating neighbors" 		      
        for neighbor in current.neighbors:
#            print "currkey=%g, neighbkey=%g" % (current.key, neighbor.key)
            if (not neighbor.finished) and (neighbor.key > (current.key + 1)):
                neighbor.key = current.key + 1
#                print "new neighbkey=%g" % (neighbor.key)
#                print "before sort " + prioq.queue[0].self_url
                prioq.queue.sort(key=attrgetter("key"))
#               print "after sort " + prioq.queue[0].self_url
                neighbor.dij_prev = current
                G.add_node(current.self_url,dist=current.key)  
                
#                print "\tadded %s" % neighbor.self_url

        #after updating as necessary, this node is in "finished" pile
        current.finished = True
        
        
    	G.add_node(current.self_url,status="finished",dist=current.key)
    	if current.dij_prev != None:
            G[current.self_url][current.dij_prev.self_url]["type"]="finished"
       	    	
        
        pq_pop(prioq)
        
    return G, dij_path
