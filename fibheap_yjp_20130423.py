# this combines cindy and jeanette's work thus far

# this class represents a node within a tree within a Fibonacci heap;
#   i.e., the actual elements of the heap
# it contains fields for the necessary key, value, and children data,
#   but also has fields to describe its relationship with its sibling
#   nodes as well as its markedness status
# it contains methods for adding to and cutting children from this node

class TreeNode(object): 
    def __init__(self, key, url) :
        #the key contains the distance value
        self.key = key
        #this contains the url string of itself
        self.self_url = url
        # this contains the list of neighbors (e.g., list of tnodes corresponding to urls that I link to)
        # list will be list of refs to these tnodes
        self.neighbors = []
        #this contains a ref to the tnode which leads back to the starting url in the most shortest route
        self.dij_prev = None
        # this means that it was processed through Dijkstra's
        self.finished = False
        # the following are fib heap requirements
        self.prev = None
        self.next = None
        self.children = []
        self.marked = False
        # added pointer to parent, if any
        self.parent = None

    # adds a child to this parent node, updating its linked-list of children
    # O(1)
    def add_child(self,new_child) :
        if len(self.children) > 0 :
            # new_child's 'prev' should point to end of children list
            new_child.prev = self.children[-1]
            # new_child's 'next' should be the same as last child's
            # 'next' (e.g., None)
            new_child.next = self.children[-1].next
            # last child's next now points to the new child
            self.children[-1].next = new_child
        # new child points to parent
        new_child.parent = self
        #actually add the child to the children list
        self.children.append(new_child)

    # cuts a child, updating linked-list of children and returning cut node
    # also sets this node's marked status to TRUE
    # O(n) where n = len(self.children)
    def cut_child(self,cut_index) :
        # in case of out-of-bound values for cut_index
        if cut_index >= len(self.children) or cut_index < 0 :
            return None
            
        if cut_index+1 < len(self.children) and cut_index > 0 :
            # connect (child after the one to be cut) to
            # (child before the one to be cut)
            self.children[cut_index + 1].prev = self.children[cut_index - 1]
            # connect (child before the one to be cut) to
            # (child after the one to be cut)
            self.children[cut_index - 1].next = self.children[cut_index + 1]
        #case of cutting the first element
        # YJP: I re-did these conditions to make them simpler and more correct, but
        # if they get screwed up, replace with prev version
        elif cut_index+1 <= len(self.children)-1 and cut_index - 1 < 0:
            self.children[1].prev = None
        # case of cutting the last element
        elif cut_index+1 > len(self.children)-1 and cut_index -1 >=0 :
            self.children[cut_index-1].next = None        
        
        # remove that child from the list
        # (now that links are re-done to cut this out)
        new_root = self.children.pop(cut_index)
        # mark the parent
        self.marked = True
        new_root.prev = new_root
        new_root.next = new_root
        new_root.parent = None
        new_root.marked = False
        # the caller will have to take care of inserting the new root
        # into the ring of roots
        return new_root

    def print_treenode_and_children(self,tnode,s,output_f) :
        for child in tnode.children :
            print >> output_f, (s + 'Node key:' + repr(child.key))
            if len(child.children) > 0 :
                child.print_treenode_and_children(child,'\t'+s, output_f)

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
            
    def find_on_self_url(self,url) :
        #check your own url
        if self.self_url == url:
            return self
        #check all your children's recursively
        if len(self.children) > 0:
            for child in self.children:
                temp_answer = child.find_on_self_url(url)
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
        # YJP: changed this around to be consistent with other functions
        # if the node to be added is less than root, root becomes
        # child of the node to be added
        if self.root.key < tnode.key :
            self.root.add_child(tnode)
            self.degree += 1
        # else vice versa
        else :
            tnode.add_child(self.root)
            self = Tree(tnode)
            
    def cut(self,tnode) :
        #index returns the index pos of first occurrence of tnode in list
        new_root = self.root.cut_child(self.root.children.index(tnode))
        self.root.degree -= 1
        return Tree(new_root)
        
    # NOT SURE HOW THIS IS DIFFERENT FROM ADD (SEEMS REDUNDANT, 
    # 3RD LINE MIGHT BE WRONG)
    # ** Ans: add inserts a treenode into a tree; merge combines two trees.
    # **      If anything, add is a helper function for merge, which
    # **      is primarily what we'll be using in FibHeap.
    def merge_with(self,tree) :
        if self.root.key < tree.root.key :
            self.add(tree.root)
            return self
        else :
            tree.add(self.root)
            return tree
    
    def print_tree(self, output_f):
        print >> output_f,('Tree root:' +repr(self.root.key))
        print >> output_f, "Tree degree: %d" % self.degree
        self.root.print_treenode_and_children(self.root,'', output_f)

# this class represents a node of the linked list at the core of the Fibonacci
# heap; it is a wrapper for the tree that is the actual list element
# it contains the tree as well as fields to maintain the doubly linked list
# it contains methods to look at the key at the top of its tree and to merge
# itself with another CircNode

# YJP interpretation: this is the root node that are connected to other 
# root nodes in a doubly-linked circle 

class CircNode(object) :
    def __init__(self, tree) :
        tree.root.marked = False
        tree.root.parent = None
        tree.root.prev = tree.root.next = tree.root
        self.tree = tree
        self.prev = self.next = self

    def key(self):
        return self.tree.root.key

    def merge(self,other_node) :
        self.tree = self.tree.merge_with(other_node.tree)

# the actual Fibonacci heap
# contains only a reference to the min CircNode in the heap
# ** AND THE SIZE OF THE CORE DOUBLY-LINKED LIST
# ** (for convenience and to prevent infinite looping)
class FibHeap(object) :
    def __init__(self) :
        self.min = None
        self.size = 0

    # returns whether or not this heap is empty
    def is_empty(self) :
        return self.min == None

    # inserts the given TreeNode into the heap ("adds a new tree")
    def insert(self,tnode) :
        cnode = CircNode(Tree(tnode))
        if self.is_empty() :
            self.min = cnode
        else :
            # always insert cnode before the current min
            cnode.prev = self.min.prev
            cnode.next = self.min
            self.min.prev.next = cnode
            self.min.prev = cnode
            if (cnode.tree.root.key < self.min.tree.root.key):
                 self.min = cnode
        self.size += 1
			
    # returns the minimum element of the heap (as a TreeNode) without
    #   removing it
    def get_min(self):
        return self.min.tree.root

    # returns the minimum element of the heap (as a TreeNode) and removes
    # it from the heap
    def pop(self) :
        if self.is_empty() :
            return None
        returnval = self.min.tree.root
        if (self.size == 1) && (self.min.tree.degree == 0):
            self.min = None
        else :
            num_children = len(self.min.tree.root.children)
            if self.min.tree.degree != num_children :
                print "key = %g, degree = %d, num children = %d" % (
                    self.min.tree.root.key, self.min.tree.degree, num_children)
            if self.min.tree.degree == 0 :
                self.min.prev.next = self.min.next
                self.min.next.prev = self.min.prev
            else :
                self.min.tree.root.children[0].parent = None
                new_head = CircNode(Tree(self.min.tree.root.children[0]))
                new_tail = new_head
                if self.min.tree.degree > 1 :
                    curr_child = new_head
                    for child in self.min.tree.root.children[1:] :
                        child.parent = None
                        curr_child.next = CircNode(Tree(child))
                        curr_child.next.prev = curr_child
                        curr_child = curr_child.next
                        if child == self.min.tree.root.children[-1] :
                            new_tail = curr_child
                self.min.prev.next = new_head
                new_head.prev = self.min.prev
                self.min.next.prev = new_tail
                new_tail.next = self.min.next
        self.size += len(self.min.tree.root.children) - 1
        self.min = self.min.next
        self.restructure()
        return returnval

    # restructures the heap's core double-linked-list after the removal
    #   of one of the heap's elements
    def restructure(self) :
        if not self.is_empty() :
            degrees = [None]
            max_degree = len(degrees) - 1
            currCNode = self.min
            while True :
                if currCNode.tree.degree > max_degree :
                    for i in range (max_degree, currCNode.tree.degree) :
                        degrees.append(None)
                if degrees[currCNode.tree.degree] == currCNode :
                    break
                elif degrees[currCNode.tree.degree] == None :            
                    degrees[currCNode.tree.degree] = currCNode
                    currCNode = currCNode.next
                else :
                    mergeNode = self.remove_node(degrees[currCNode.tree.degree])
                    degrees[currCNode.tree.degree] = None
                    currCNode.merge(mergeNode)
                    if self.min == mergeNode :
                        self.min = currCNode
                    self.size -= 1
                    

    def remove_node(self, cnode) :
        cnode.prev.next = cnode.next
        cnode.next.prev = cnode.prev
        cnode.prev = cnode.next = cnode
        return cnode

    # decreases the key of the given TreeNode to the specified value,
    # cutting children off into new trees if the min-heap invariant becomes
    # violated in the new configuration
    def decr_key(self, tnode, new_key) :
        print "decr-ing tnode %g to %g" % (tnode.key,new_key)
        if new_key >= tnode.key :
            raise InvalidKey("New key must be less than old key")
        else :
            tnode.key = new_key
            if (tnode.parent != None) :
                if (tnode.key < tnode.parent.key) :
                    self.fix_heap_recursive(tnode)
            else :
                self.reset_min(self.min)

    def fix_heap_recursive(self, tnode) :
        if tnode.parent != None :
            theParent = tnode.parent
            parent_marked = theParent.marked
            new_root = theParent.cut_child(theParent.children.index(tnode))
            self.insert(new_root)
            if parent_marked :
                self.fix_heap_recursive(theParent)

    def reset_min(self,circnode) : 
        start_circnode = circnode
        curr_circnode = circnode
        temp_min = circnode
        while True :
            if curr_circnode.next is start_circnode:
                break
            elif curr_circnode.next.tree.root.key < temp_min.tree.root.key :
                temp_min = curr_circnode.next
            curr_circnode = curr_circnode.next
        return temp_min

    # removes the given TreeNode from the heap (does not return the node)
    def delete(self,tnode) :
        self.decr_key(tnode, float("-inf"))
        self.pop()

    # merges this heap with another Fibonacci heap
    def merge(self,other_heap) :
        other_heap.min.prev.next = self.min.next
        self.min.next.prev = other_heap.min.prev
        self.min.next = other_heap.min
        other_heap.min.prev = self.min
        if other_heap.min.tree.root.key < self.min.tree.root.key :
            self.min = other_heap.min
        self.size += other_heap.size

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

    def find_on_self_url(self,url) :
        #if heap is entirely empty, then return None
        if self.is_empty() :
            return None
        start_circnode = self.min
        curr_circnode = self.min
        answer_tnode = curr_circnode.tree.root.find_on_self_url(url)
        if answer_tnode != None:
            return answer_tnode
        while True:
            if curr_circnode.next == start_circnode :
                return None
            curr_circnode = curr_circnode.next 
            answer_tnode = curr_circnode.tree.root.find_on_self_url(url)
            if answer_tnode != None:
                return answer_tnode   
                
    # yjp: prints all the nodes in the heap, and use for testing
    def print_heap (self, output_f) :
        print >> output_f, "\nThis is a heap of size" + repr(self.size) + "and min:" + repr(self.min.tree.root.key)
        curr_circnode = self.min
        for i in range(-1,self.size) :
            print >> output_f, "\nthis is a circnode:"
            curr_circnode.tree.print_tree(output_f)
            curr_circnode = curr_circnode.next

    def print_CDDL(self, output_f) :
        print >> output_f, "\nHeap CDDL:"
        curr_circnode = self.min
        for i in range(-1,self.size) :
            print >> output_f, "Circnode " + repr(curr_circnode.tree.root.key)
            curr_circnode = curr_circnode.next
