# this class represents a node within a tree within a Fibonacci heap;
#   i.e., the actual elements of the heap
# it contains fields for the necessary key, value, and children data,
#   but also has fields to describe its relationship with its sibling
#   nodes as well as its markedness status
# it contains methods for adding to and cutting children from this node

class TreeNode(object): 
    def __init__(self, k, v) :
        self.key = k
        # change below from "value" to "v"; also, this should be a pointer to the 
        # corresponding element in the overarching list of all vertices
        self.val = v
        self.prev = None
        self.next = None
        self.children = []
        self.marked = False
        # added pointer to parent, if any
        self.parent = None

    # adds a child to this parent node, updating its linked-list of children
    # O(1)
    def add_child(self,new_child) :
        #actually add the child to the children list
        self.children.append(new_child)
        # new_child's 'prev' should point to end of children list
        new_child.prev = self.children[-1]
        # new_child's 'next' should be the same as last child's 'next' (e.g., None)
        new_child.next = self.children[-1].next
        # last child's next now points to the new child
        self.children[-1].next = new_child
        # new child points to parent
        new_child.parent = self

    # cuts a child, updating linked-list of children and returning cut node
    # also sets this node's marked status to TRUE
    # O(n) where n = len(self.children)
    def cut_child(self,cut_index) :
        # in case of out-of-bound values for cut_index
        if cut_index+1 > len(self.children) or cut_index < 0 :
            return None
            
        if cut_index+1 <= len(self.children)-1 and cut_index -1 >=0 :
            # connect (child after the one to be cut) to (child before the one to be cut)
            self.children[cut_index + 1].prev = self.children[cut_index - 1]
            # connect (child before the one to be cut) to (child after the one to be cut)
            self.children[cut_index - 1].next = self.children[cut_index + 1]
        #case of cutting the first element
        elif cut_index+1 <= len(self.children)-1 and cut_index - 1 < 0:
            self.children[cut_index + 1].prev = None
        # case of cutting the last element
        elif cut_index+1 > len(self.children)-1 and cut_index -1 >=0 :
            self.children[cut_index-1].next = None        
        
        # remove that child from the list (now that links are re-done to cut this out
        new_tree = self.children.pop(cut_index)
        # mark the parent
        self.marked = True
        new_tree.prev = None
        new_tree.next = None
        # the caller will have to take care of inserting the new tree into the ring of roots
        return new_tree

    def print_treenode_and_children(self,tnode,s) :
        for child in tnode.children :
            print (s + 'Node key:' + repr(child.key))
            if len(child.children) > 0 :
                child.print_treenode_and_children(child,self.add_indent(s))
    
    def add_indent(self,s) :
        s += '    '
        return s
    
    def find(self,key) :
        #check your own key
        if self.key == key:
            return self
        #check all your children's recursively
        if len(self.children) > 0:
            for child in self.children:
                temp_answer = child.find(key)
                if temp_answer != None:
                    return temp_answer
        else:
            return None

# this class represents one of the trees the Fibonacci heap is a collection of
# it holds a reference to the root node of the tree and the degree of the
#   tree (number of children its root has)
# it has methods for adding to and cutting nodes from the tree, as well as
#   for merging this tree with another tree
class Tree(object) :
    def __init__(self, tnode) :
        self.root = tnode
        # degree is the number of children that the node has
        self.degree = len(self.root.children)

    def add(self,tnode) :
        # YJP: changed this around to be consistent with other functions in FibHeap
        # if the node to be added is less than root, root becomes child of the node to be added
        if self.root.key < tnode.key :
            self.root.add_child(tnode)
        # else vice versa
        else :
            tnode.add_child(self.root)

    def cut(self,tnode) :
        #index returns the index pos in the list of the first item whose value is tnode
        self.root.cut_child(self.root.children.index(tnode))

    # NOT SURE HOW THIS IS DIFFERENT FROM ADD (SEEMS REDUNDANT, 3RD LINE MIGHT BE WRONG 
    def merge_with(self,tree) :
        if self.root.key < tree.root.key :
            self.add(tree.root)
            return self
        else :
            tree.add(self.root)
            return tree
    
    def print_tree(self):
        print('Tree root:' +repr(self.root.key))
        self.root.print_treenode_and_children(self.root,'')

# this class represents a node of the linked list at the core of the Fibonacci
# heap; it is a wrapper for the tree that is the actual list element
# it contains the tree as well as fields to maintain the doubly linked list
# it contains methods to look at the key at the top of its tree and to merge
# itself with another CircNode

# YJP interpretation: this is the root node that are connected to other 
# root nodes in a doubly-linked circle 

class CircNode(object) :
    def __init__(self, tree) :
        self.tree = tree
        self.prev = None
        self.next = None

    def key(self):
        return self.tree.root.key

    def merge(self,other_node) :
        self.tree = self.tree.merge_with(other_node.tree)

# the actual Fibonacci heap
# contains only a reference to the min CircNode in the heap
class FibHeap(object) :
    def __init__(self) :
        self.min = None

    # returns whether or not this heap is empty
    def is_empty(self) :
        return self.min == None

    # inserts the given CircNode into the heap ("adds a new tree")
    def insert(self,cnode) :
        if self.is_empty() :
            #self.min points to a cnode, and self.min() returns a TreeNode
            self.min = cnode
            cnode.next = cnode
            cnode.prev = cnode
        # always insert cnode before the current min
        cnode.prev = self.min.prev
        cnode.next = self.min
        self.min.prev.next = cnode
        self.min.prev = cnode
        if (cnode.tree.root.key < self.min.tree.root.key):
            #self.min points to a cnode, and self.min() returns a TreeNode
            self.min = cnode
			
    # returns the minimum element of the heap (as a TreeNode) without
    #   removing it
    #def get_min(self):
    #    return self.min.tree.root

    # returns the minimum element of the heap (as a TreeNode) and removes
    # it from the heap
    def pop(self) :
        if self.is_empty() :
            return None
        # if there is only one circnode and only one tnode in that circnode (e.g., no children)
        elif (self.min.prev == self.min) and len(self.min.tree.root.children) == 0 :
            temp_min = self.min.tree.root
            self.min = None
            return temp_min
        else: 
            temp_min = self.min.tree.root
            #concatenate the min's children into root list
            for child in temp_min.children:
                self.insert(CircNode(Tree(child)))
            # cut out old min
            self.min.prev.next = self.min.next
            self.min.next.prev = self.min.prev
            # Choose a new self.min, looking from the right of the old self.min
            self.min = self.get_min(self.min.next)
            # consolidate trees so that no two roots have same degree
            self.min = self.get_min(self.consolidate_trees(self.min))
            #return the min saved at the beginning as TreeNode
            return temp_min

    #this method gives back the circnode that contains the min root key 
    #in the circularly linked list of trees, given any circnode in that
    # circularly linked list
    def get_min(self,circnode) : 
        start_circnode = circnode
        curr_circnode = circnode
        temp_min = circnode
        not_full_circle = True
        while True :
            if curr_circnode.next is start_circnode:
                break
            elif curr_circnode.next.tree.root.key < temp_min.tree.root.key :
                temp_min = curr_circnode.next
            curr_circnode = curr_circnode.next
        return temp_min
		
    #this method consolidates the trees so that no two roots have 
    # the same degree, and returns one of the circnodes in the 
    # circularly doubly linked list
    # check if roots_have_same_degree. if so, get degree of first circnode, 
    # then check if any other circnode
    # has same degree. if found one, consolidate. if not, get degree of second
    # circnode and do the same. once one consolidation happens, run 
    # roots_have_same_degree again. repeat until roots_have_same_degree says false
    def consolidate_trees(self,circnode):
        circnode_with_duplicate_degree = self.ring_has_two_or_more_circnodes_w_same_degree (circnode)
        circnode_i_know_is_in_circle = circnode
        while circnode_with_duplicate_degree != None :
            print '\nthis is new iteration'
            self.print_heap()
            circnode_i_know_is_in_circle = self.consolidate_trees_single (circnode_with_duplicate_degree)
            circnode_with_duplicate_degree = self.ring_has_two_or_more_circnodes_w_same_degree (circnode_i_know_is_in_circle)
        return circnode_i_know_is_in_circle
            
    # returns a circnode that has the same degree as one or more other circnodes in the ring
    # returns None otherwise
    def ring_has_two_or_more_circnodes_w_same_degree (self,circnode) :
        start_circnode = circnode
        curr_circnode = circnode
        if self.another_circnode_w_same_degree_as_this (start_circnode) :
            return start_circnode
        else:
            while True:
                if curr_circnode.next is start_circnode:
                    return None
                else:
                    curr_circnode = curr_circnode.next
                    if self.another_circnode_w_same_degree_as_this (curr_circnode) :
                        return curr_circnode            
    
    # runs through the circular doubly linked list of roots and returns 
    # False if there are no circnodes with the same degree as the ARGUMENT and else, true
    def another_circnode_w_same_degree_as_this(self,circnode):
        start_circnode = circnode
        start_circnode_degree = len(start_circnode.tree.root.children)
        curr_circnode = circnode
        while True:
            if curr_circnode.next is start_circnode :
                return False
            else :
                curr_circnode = curr_circnode.next
                if len(curr_circnode.tree.root.children) == start_circnode_degree :
                    return True
    
    def consolidate_trees_single (self,circnode):
        start_circnode = circnode
        start_circnode_degree = len(start_circnode.tree.root.children)
        curr_circnode = circnode
        while True: 
            curr_circnode = curr_circnode.next
            if len(curr_circnode.tree.root.children) == start_circnode_degree:
                if curr_circnode.key() < start_circnode.key() :
                    #curr_circnode will end up staying in the circular doubly linked list
                    #so cut out start_circnode from the circle
                    start_circnode.prev.next = start_circnode.next
                    start_circnode.next.prev = start_circnode.prev
                    #and merge in the start_circnode
                    start_circnode.merge (curr_circnode)
                    return curr_circnode
                else:
                    curr_circnode.prev.next = curr_circnode.next
                    curr_circnode.next.prev = curr_circnode.prev
                    curr_circnode.merge (start_circnode)
                    return start_circnode
						
    # decreases the key of the given TreeNode to the specified value
    def decr_key(self,tnode, new_key) :
        pass

    # removes the given TreeNode from the heap (does not return the node)
    def delete(self,tnode) :
        pass

    # merges this heap with another Fibonacci heap
    def merge(self,other_heap) :
        pass

    # returns the TreeNode with the given key, or None if key not in heap
    def find(self,key) :
        start_circnode = self.min
        curr_circnode = self.min
        answer_tnode = curr_circnode.tree.root.find(key)
        if answer_tnode != None:
            return answer_tnode
        while True:
            if curr_circnode.next == start_circnode :
                return None
            curr_circnode = curr_circnode.next 
            answer_tnode = curr_circnode.tree.root.find(key)
            if answer_tnode != None:
                return answer_tnode
            
        
    # restructures the heap's core double-linked-list after the removal
    #   of one of the heap's elements
    # REMOVED BECAUSE LIKE CONSOLIDATE TREES
    #def restructure(self) :
    #    pass
        
    # yjp: prints all the nodes in the heap, and use for testing
    def print_heap (self) :
        start_circnode = self.min
        curr_circnode = self.min
        print ('this is a circnode:')
        curr_circnode.tree.print_tree()
        while curr_circnode.next is not start_circnode :
            print ('\nthis is a circnode:')
            curr_circnode = curr_circnode.next
            curr_circnode.tree.print_tree()

        
