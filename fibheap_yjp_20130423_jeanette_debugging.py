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
    def add_child(self,new_child,output_f) :
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
    def cut_child(self,cut_index,output_f) :
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
        #self.marked = True
        new_root.prev = new_root
        new_root.next = new_root
        new_root.parent = None
        new_root.marked = False
        # the caller will have to take care of inserting the new root
        # into the ring of roots
        return new_root

    def print_treenode_and_children(self,tnode,s,output_f) :
        for child in tnode.children :
            print >> output_f, (s + 'Node key:' + repr(child.key)+ 'Self_url:' + repr(child.self_url) + 'Number of neighbors' + repr(len(child.neighbors)))
            if len(child.children) > 0 :
                child.print_treenode_and_children(child,'\t'+s, output_f)

    def find(self,key,output_f) :
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
            
    def find_on_self_url(self,url,output_f) :
        #check your own url
        if self.self_url == url:
            return self
        #check all your children's recursively
        if len(self.children) > 0:
            for child in self.children:
                temp_answer = child.find_on_self_url(url,output_f)
                if temp_answer != None:
                    return temp_answer
            return None

# this class represents one of the trees the Fibonacci heap is a collection of
# it holds a reference to the root node of the tree and the degree of the
#   tree (number of children its root has)
# it has methods for adding to and cutting nodes from the tree, as well as
#   for merging this tree with another tree
class Tree(object) :
    def __init__(self, tnode) :
        self.root = tnode
    
    def __getattr__(self, attr):
        if attr == "degree":
            return len(getattr(self.root,"children"))
        # degree is the number of children that the node has
        #self.degree = len(self.root.children)

    def add(self,tnode,output_f) :
        # YJP: changed this around to be consistent with other functions
        # if the node to be added is less than root, root becomes
        # child of the node to be added
        self.root.add_child(tnode, output_f)
        # I don't think this is necessary b/c degree is read as len of children list
        #self.degree += 1
            
    def cut(self,tnode,output_f) :
        #index returns the index pos of first occurrence of tnode in list
        new_root = self.root.cut_child(self.root.children.index(tnode),output_f)
        #self.root.degree -= 1
        return Tree(new_root)
        
    # NOT SURE HOW THIS IS DIFFERENT FROM ADD (SEEMS REDUNDANT, 
    # 3RD LINE MIGHT BE WRONG)
    # ** Ans: add inserts a treenode into a tree; merge combines two trees.
    # **      If anything, add is a helper function for merge, which
    # **      is primarily what we'll be using in FibHeap.
    def merge_with(self,tree,output_f) :
        if self.root.key < tree.root.key :
            self.add(tree.root,output_f)
            return self
        else :
            tree.add(self.root,output_f)
            return tree
    
    def print_tree(self, output_f):
        print >> output_f,('Tree root:' +repr(self.root.key)+ 'Tree root self_url:' + repr(self.root.self_url) + 'Tree root number of neighbors: ' + repr(len(self.root.neighbors)))
        print >> output_f, "Tree degree:" + repr(self.degree)
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
        self.checked_for_consolidation = False

    def key(self,output_f):
        return self.tree.root.key

    def merge(self,other_node,output_f) :
        lower_key_tree = self.tree.merge_with(other_node.tree,output_f)

# the actual Fibonacci heap
# contains only a reference to the min CircNode in the heap
# ** AND THE SIZE OF THE CORE DOUBLY-LINKED LIST
# ** (for convenience and to prevent infinite looping)
class FibHeap(object) :
    def __init__(self) :
        self.min = None
        #the below refers to number of nodes in the core doubly-linked list/ ring
        self.size = 0
        # the below refers to total number of nodes in the fibheap (not just in the ring)
        self.total_size = 0

    # returns whether or not this heap is empty
    def is_empty(self,output_f) :
        return self.min == None

    # inserts the given TreeNode into the heap ("adds a new tree")
    def insert(self,tnode,output_f) :
        tnode.parent = None
        cnode = CircNode(Tree(tnode))
        if self.is_empty(output_f) :
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
        self.total_size += 1
        print>> output_f, "after an insert*************"
        self.print_heap(output_f)
        return cnode
			
    # returns the minimum element of the heap (as a TreeNode) without
    #   removing it
    def get_min(self,output_f):
        return self.min.tree.root

    # returns the minimum element of the heap (as a TreeNode) and removes
    # it from the heap
    def pop(self,output_f) :
        print>> output_f, "\npop happened ***************"
        if self.is_empty(output_f) :
            return None
        else :
            returnval = self.min.tree.root
            # there is only one cnode left and it has no children
            if (self.min.next is self.min) and self.min.tree.degree == 0:
                self.min = None
                self.total_size -=1
                self.size -=1
                return returnval
            # min is not the only cnode left but min has no children
            elif (self.min.next is not self.min) and self.min.tree.degree == 0:
                self.min.prev.next = self.min.next
                self.min.next.prev = self.min.prev
                self.min = self.min.next
                self.restructure(output_f)
                self.total_size -= 1
                self.size -= 1
                return returnval
            # min is the only cnode left and it has children
            elif self.min.next is self.min:
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
                new_head.prev = new_tail
                new_tail.next = new_head
                self.size += (len(self.min.tree.root.children) - 1)
                self.total_size -= 1
                self.min = new_head
                self.restructure(output_f)
                return returnval
            # min is not the only cnode left and it has children
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
                self.size += (len(self.min.tree.root.children) - 1)
                self.total_size -= 1
                self.min = new_head
                self.restructure(output_f)
                return returnval                

    # restructures the heap's core double-linked-list after the removal
    # of one of the heap's elements (circnode ring exists but 
    # consolidation hasn't happened yet
    # also, haven't set a new, correct self.min yet
    def restructure(self,output_f) :
        degrees = [None]
        currCNode = self.min
        while True :
            #the largest degree that we are tracking
            max_degree = len(degrees) - 1
            #to get the right min by the end
            temp_min_key = self.min.key(output_f)
            if currCNode.key(output_f) <= temp_min_key:
                self.min = currCNode
                temp_min_key = self.min.key(output_f)
            # if we run across a cnode with a degree larger than we are tracking
            if currCNode.tree.degree > max_degree :
                print>>output_f, "THIS IS THE PROBLEM AREA!! (A)**********"
                for i in range (max_degree, currCNode.tree.degree) :
                    degrees.append(None)
                degrees[currCNode.tree.degree] = currCNode
                currCNode = currCNode.next
                continue
            # if we have come all the way back to the same cnode, and the next cnode has been checked to have no duplicates either, we've run the whole ring
            if degrees[currCNode.tree.degree] is currCNode :
                print>>output_f, "THIS IS THE PROBLEM AREA!! (B)**********"
                currCNode.checked_for_consolidation = True
                if currCNode.next.checked_for_consolidation == True:
                    break
                else:
                    currCNode = currCNode.next
                    continue
            if degrees[currCNode.tree.degree] == None :
                print>>output_f, "THIS IS THE PROBLEM AREA!! (C)**********"
                degrees[currCNode.tree.degree] = currCNode
                currCNode = currCNode.next
            else :
                #this is the cnode prev identified as one having same degree as our current cnode
                mergeNode = degrees[currCNode.tree.degree]
                degrees[currCNode.tree.degree] = None
                if mergeNode.key(output_f) < currCNode.key(output_f):
                    print>>output_f, "THIS IS THE PROBLEM AREA!! (D)**********"
                    print>>output_f, "mergeNode is " + repr(mergeNode.tree.root.self_url) + "with key " + repr(mergeNode.tree.root.key) + "and with degree " + repr(mergeNode.tree.degree)
                    print>>output_f, "currCNode is " + repr(currCNode.tree.root.self_url) + "with key " + repr(currCNode.tree.root.key) + "and with degree " + repr(currCNode.tree.degree)
                    mergeNode.prev.next = mergeNode.next
                    mergeNode.next.prev = mergeNode.prev
                    mergeNode.next = currCNode.next
                    mergeNode.prev = currCNode.prev
                    currCNode.prev.next = mergeNode
                    currCNode.next.prev = mergeNode
                    mergeNode.tree.root.add_child(currCNode.tree.root,output_f)
                    if currCNode is self.min:
                        self.min = mergeNode
                    currCNode = mergeNode
                else:
                    print>>output_f, "THIS IS THE PROBLEM AREA!! (E)**********"
                    self.remove_node(mergeNode,output_f)
                    currCNode.tree.root.add_child(mergeNode.tree.root,output_f)
                    if mergeNode is self.min:
                        self.min = currCNode
                currCNode.checked_for_consolidation = False
                self.size -= 1
            print>>output_f, "\nafter one iteration of restructure*******************"
            self.print_heap(output_f)
                            
    def remove_node(self, cnode,output_f) :
        cnode.prev.next = cnode.next
        cnode.next.prev = cnode.prev
        cnode.prev = cnode.next = cnode
        return cnode

    # decreases the key of the given TreeNode to the specified value,
    # cutting children off into new trees if the min-heap invariant becomes
    # violated in the new configuration
    def decr_key(self, tnode, new_key, output_f) :
        print >> output_f, "Decr_key happened! ********************"
        #print "decr-ing tnode %g to %g" % (tnode.key,new_key)
        if new_key >= tnode.key :
            raise InvalidKey("New key must be less than old key")
        else :
            tnode.key = new_key
            if (tnode.parent != None) :
                if (tnode.key < tnode.parent.key) :
                    #fix_heap uses insert, which should update the min 
                    self.fix_heap_recursive(tnode, output_f)
            else :
                self.reset_min(self.min,output_f)
    
    def fix_heap_recursive(self, tnode, output_f) :
        if tnode.parent != None :
            theParent = tnode.parent
            parent_marked = theParent.marked
            new_root = theParent.cut_child(theParent.children.index(tnode),output_f)
            self.insert(new_root, output_f)
            # before, when you marked the parent in cut_child, you always get a parent_marked (e.g., never a case 1 in ppt)
            if parent_marked :
                self.fix_heap_recursive(theParent,output_f)
            else:
                theParent.market = True

    def reset_min(self,circnode,output_f) : 
        start_circnode = circnode
        curr_circnode = circnode
        temp_min = circnode
        while True :
            if curr_circnode.next is start_circnode:
                break
            elif curr_circnode.next.tree.root.key < temp_min.tree.root.key :
                temp_min = curr_circnode.next
            curr_circnode = curr_circnode.next
        self.min = temp_min

    # removes the given TreeNode from the heap (does not return the node)
    def delete(self,tnode, output_f) :
        self.decr_key(tnode, float("-inf"), output_f)
        self.pop(output_f)

    # merges this heap with another Fibonacci heap
    def merge(self,other_heap,output_f) :
        other_heap.min.prev.next = self.min.next
        self.min.next.prev = other_heap.min.prev
        self.min.next = other_heap.min
        other_heap.min.prev = self.min
        if other_heap.min.tree.root.key < self.min.tree.root.key :
            self.min = other_heap.min
        self.size += other_heap.size
        #YJP: also added below
        self.total_size += other_heap.total_size

    # returns the TreeNode with the given key, or None if key not in heap
    def find(self,key,output_f) :
        start_circnode = self.min
        curr_circnode = self.min
        answer_tnode = curr_circnode.tree.root.find(key,output_f)
        if answer_tnode != None:
            return answer_tnode
        while True:
            if curr_circnode.next == start_circnode :
                return None
            curr_circnode = curr_circnode.next 
            answer_tnode = curr_circnode.tree.root.find(key,output_f)
            if answer_tnode != None:
                return answer_tnode

    def find_on_self_url(self,url,output_f) :
        #if heap is entirely empty, then return None
        if self.is_empty(output_f) :
            return None
        start_circnode = self.min
        curr_circnode = self.min
        answer_tnode = curr_circnode.tree.root.find_on_self_url(url,output_f)
        if answer_tnode != None:
            return answer_tnode
        while True:
            if curr_circnode.next == start_circnode :
                return None
            curr_circnode = curr_circnode.next 
            answer_tnode = curr_circnode.tree.root.find_on_self_url(url,output_f)
            if answer_tnode != None:
                return answer_tnode   
                
    # yjp: prints all the nodes in the heap, and use for testing
    def print_heap (self, output_f) :
        print >> output_f, "\nThis is a heap of total size" + repr(self.total_size)
        print >> output_f, "This is key of min cnode" + repr(self.min.key(output_f))
        curr_circnode = self.min
        print >> output_f, "\nthis is a circnode:"
        curr_circnode.tree.print_tree(output_f)
        while curr_circnode.next is not self.min:
            curr_circnode = curr_circnode.next
            print >> output_f, "\nthis is a circnode:"
            curr_circnode.tree.print_tree(output_f)
            

    def print_CDDL(self, output_f) :
        print >> output_f, "\nHeap CDDL:"
        curr_circnode = self.min
        print >> output_f, "Circnode " + repr(curr_circnode.tree.root.key)
        while curr_circnode.next is not self.min:
            curr_circnode = curr_circnode.next
            print >> output_f, "Circnode " + repr(curr_circnode.tree.root.key)
            
