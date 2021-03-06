# this pulls in the dictionary generated by simple_crawler_modified.py
# and returns a doubly-linked ring of tnodes, one tnode for each unique url
# with pointer to starting url and fields for each tnode set to the default values

from fibheap_yjp_20130429_wiki import *
from simple_crawler_modified_20130429_wiki import *

# just assume for now that you will be passed a dict
# returns a heapq
def from_dict_to_heapq_urlset(dict,starting_url,output_f) :
    heap = []
    urlset = set()
    #first key is going to be the start url -> initiate with 0 distance (key)
    is_start_url = True
    for key in dict:
        urlset.add(key.lower())
        if key == starting_url and is_start_url:
            key_tnode = TreeNode(0, key.lower())
            heapq.heappush(heap, key_tnode)
            is_start_url = False
        else:
###            # check if tnode already exists in circnode ring
            key_tnode = fibheap.find_on_self_url(key.lower(),output_f)        
            # if it doesn't, add it
            if key_tnode == None :
                key_tnode = TreeNode(float("inf"), key.lower())
                fibheap.insert(key_tnode,output_f)
        # for each of the urls in its val, check if tnode already exists in circnode ring
        for val_url in dict[key]:
            urlset.add(val_url.lower())
            val_tnode = fibheap.find_on_self_url(val_url.lower(),output_f)
            # if it doesn't exist, add the tnode
            if val_tnode == None:
                val_tnode = TreeNode(float("inf"), val_url.lower())
                fibheap.insert(val_tnode,output_f)
            # the connect this val_url tnode to key tnode
            key_tnode.neighbors.append(val_tnode)
    return fibheap, urlset
        