#!/usr/bin/python  
from dict_to_tnodes import * 

        
#algorithm to find the shortest path from the home page 
#(min node of the heap) to the destination url
#takes in the fibheap generated from the starting link
#and the url of the desired destination

def findShortestPath(fibheap,destination): 
    output_for_debugging_dij = open("output_for_debugging_dij.txt", "w+") 
    print ("Starting shortest path...")
    print (fibheap.is_empty())
    while not fibheap.is_empty():
        # set current node
        current = fibheap.min.tree.root
        print "this is url of fibheap min" + (fibheap.min.tree.root.self_url) 
        print "fibheap 'size' is: " + repr(fibheap.size)           
        print "number of children of min is: " + repr(len(fibheap.min.tree.root.children))
        if current.self_url == destination:
                print "Shortest path from starting url to destination url is" + repr(current.key) + "steps"
                # print out shortest path back to starting url 
                current_tnode_printed = current
                while current_tnode_printed.dij_prev != None:
                    print current_tnode_printed.self_url
                    current_tnode_printed = current_tnode_printed.prev
                print current_tnode_printed.self_url  
                break
                
        #updating distances of neighbors, if necessary  		      
        for neighbor in current.neighbors:
            if (not neighbor.finished) and (neighbor.key > (current.key +1)):
                fibheap.decr_key(neighbor,current.key +1)
                neighbor.dij_prev = current
                
        #after checking all neighbors and updating as necessary, this node is in "finished" pile
        current.finished = True
        
        fibheap.pop()