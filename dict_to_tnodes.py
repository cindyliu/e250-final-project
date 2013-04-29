# this pulls in the dictionary generated by simple_crawler_modified.py
# and returns a doubly-linked ring of tnodes, one tnode for each unique url
# with pointer to starting url and fields for each tnode set to the default values

from fibheap_yjp_20130423_jeanette_debugging import *
from simple_crawler_modified import *

# just assume for now that you will be passed a dict
# returns a fibheap
def from_dict_to_fibheap(dict,starting_url,output_f) :
    fibheap = FibHeap()
    #first key is going to be the start url -> initiate with 0 distance (key)
    is_start_url = True
    for key in dict:
        if key == starting_url and is_start_url:
            key_tnode = TreeNode(0, key.lower())
            fibheap.insert(key_tnode, output_f)
            is_start_url = False
        else:
            # check if tnode already exists in circnode ring
            key_tnode = fibheap.find_on_self_url(key.lower(),output_f)        
            # if it doesn't, add it
            if key_tnode == None :
                key_tnode = TreeNode(float("inf"), key.lower())
                fibheap.insert(key_tnode,output_f)
        # for each of the urls in its val, check if tnode already exists in circnode ring
        for val_url in dict[key]:
            val_tnode = fibheap.find_on_self_url(val_url,output_f)
            # if it doesn't exist, add the tnode
            if val_tnode == None:
                val_tnode = TreeNode(float("inf"), val_url.lower())
                fibheap.insert(val_tnode,output_f)
            # the connect this val_url tnode to key tnode
            key_tnode.neighbors.append(val_tnode)
    return fibheap
        