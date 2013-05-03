#!/usr/bin/python  
from dict_to_tnodes_prioqueue_20130429_wiki import * 
        
#algorithm to find the shortest path from the home page 
#(min node of the heap) to the destination url
#takes in the fibheap generated from the starting link
#and the url of the desired destination

def findShortestPath_PQ(prioq,destination): 
    print ("Starting shortest path...")
    print (prioq.empty())
    while not prioq.empty() :
        # set current node
        current = prioq.queue[0]
#        print "\nthis is url of prioqueue min: " + (prioq.queue[0].self_url) 
#        print "this is key/dist of prioqueue min: " + repr(prioq.queue[0].key)
#        print "prioqueue total size is: " + repr(prioq.qsize())
        if current.self_url == destination.lower():
                print "Shortest path from starting url to destination url is " + repr(current.key) + " steps"
                # print out shortest path back to starting url 
                current_tnode_printed = current
                while current_tnode_printed.dij_prev != None:
                    print current_tnode_printed.self_url
                    current_tnode_printed = current_tnode_printed.dij_prev
                print current_tnode_printed.self_url  
                break

        #updating distances of neighbors, if necessary
#        print "updating neighbors" 		      
        for neighbor in current.neighbors:
            if (not neighbor.finished) and (neighbor.key > (current.key + 1)):
                neighbor.key = current.key + 1
                prioq.queue.sort(key=attrgetter("key"))
                neighbor.dij_prev = current
#                print "\tadded %s" % neighbor.self_url

        #after updating as necessary, this node is in "finished" pile
        current.finished = True
        
        prioq.get_nowait()