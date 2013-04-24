# this pulls in the dictionary generated by simple_crawler_modified.py
# and returns a doubly-linked ring of tnodes, one tnode for each unique url
# with pointer to starting url and fields for each tnode set to the default values

from fibheap_yjp_20130422_1200 import *
from simple_crawler_modified import *

# just assume for now that you will be passed a dict
# returns a fibheap
def from_dict_to_fibheap(dict,starting_url) :
    fibheap = FibHeap()
    #first key is going to be the start url -> initiate with 0 distance (key)
    is_start_url = True
    for key in dict:
        if key == starting_url:
            key_tnode = TreeNode(key,0)
            fibheap.insert(CircNode(Tree(key_tnode)))
            is_start_url = False
        else:
            # check if tnode already exists in circnode ring
            key_tnode = fibheap.find_on_self_url(key)        
            # if it doesn't, add it
            if key_tnode == None :
                key_tnode = TreeNode(key, float("inf"))
                fibheap.insert(CircNode(Tree(key_tnode)))
            # for each of the urls in its val, check if tnode already exists in circnode ring
        for val_url in dict[key]:
            val_tnode = fibheap.find_on_self_url(val_url)
            # if it doesn't exist, add the tnode
            if val_tnode == None:
                val_tnode = TreeNode(val_url, float("inf"))
                fibheap.insert(CircNode(Tree(val_tnode)))
            # the connect this val_url tnode to key tnode
            key_tnode.neighbors.append(val_tnode)
    return fibheap
        
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
    fibheap.print_heap(output_f)
    print >> output_f, "\n this is the min of the heap" + fibheap.min.tree.root.self_url
    
if __name__ == "__main__":
    main()