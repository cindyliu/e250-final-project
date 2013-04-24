
  #!/usr/bin/python  
from dict_to_tnodes import * 

        
#algorithm to find the shortes path from the home page 
#(min node of the heap) to the destination url
#takes in the fibheap generated from the starting link
#and the url of the desired destination

def findShortestPath(fibheap,destination): 
 	print ("Starting shortest path")
	while not fibheap.is_empty: 
	   	print ("We're in!")
       		# set root node
       		root = fibheap.min.tree.root
       		print (root.self_url)
       
       		if root.self_url == destination:
       			print ("Found shortest path as: ")
       			return root
       			break
       	
      		 #updating distances by 1 and prev fields to root node. 		      
       		for neighbor in root.neighbors:
         		if (not neighbor.finished) & (neighbor.key > (neighbor.key +1)):
       				fibheap.decr_key(neighbor,neighbor.key +1)
       			       		
       			neighbor.dij_prev = root
       			
       		root.finished = true
       		
       		#Popping off the root of the heap
      		fibheap.pop()
       
    
def main():  

       
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth = opts.depth

   
    crawler = Crawler(url, depth)
    crawler.crawl()
    dict = crawler.urls
    #create ring of one-node circnodes with the urls found
    fibheap = from_dict_to_fibheap(dict, url)
    
    print('Starting Dijkstra\'s Algorithm...')       
     
    findShortestPath (fibheap,'http://en.wikipedia.org/wiki/Peafowl')
    
    
      
main()  