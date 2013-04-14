# this class represents a node within a tree within a Fibonacci heap;
#   i.e., the actual elements of the heap
# it contains fields for the necessary key, value, and children data,
#   but also has fields to describe its relationship with its sibling
#   nodes as well as its markedness status
# it contains methods for adding to and cutting children from this node
class TreeNode(object): 
    def __init__(self, k, v) :
        self.key = k
        self.val = value
        self.prev = None
        self.next = None
        self.children = []
        self.marked = False

    # adds a child to this parent node, updating its linked-list of children
    # O(1)
    def add_child(new_child) :
        new_child.prev = self.children[-1]
        new_child.next = self.children[-1].next
        self.children[-1].next = new_child
        self.children.append(new_child)

    # cuts a child, updating linked-list of children and returning cut node
    # also sets this node's marked status to TRUE
    # O(n) where n = len(self.children)
    def cut_child(cut_index) :
        self.children[cut_index + 1].prev = self.children[cut_index - 1]
        self.children[cut_index - 1].next = self.children[cut_index + 1]
        new_tree = self.children.pop(cut_index)
        self.marked = True
        new_tree.prev = None
        new_tree.next = None
        return new_tree


# this class represents one of the trees the Fibonacci heap is a collection of
# it holds a reference to the root node of the tree and the degree of the
#   tree (number of children its root has)
# it has methods for adding to and cutting nodes from the tree, as well as
#   for merging this tree with another tree
class Tree(object) :
    def __init__(self, tnode) :
        self.root = tnode
        self.degree = len(self.root.children)

    def add(tnode) :
        if tnode.key < self.root.key :
            tnode.add_child(self.root)
        else :
            self.root.add_child(tnode)

    def cut(tnode) :
        self.root.cut_child(self.root.children.index(tnode))

    def merge_with(tree) :
        if self.root.key < tree.root.key :
            add(tree.root.key)
            return self
        else :
            tree.add(self.root)
            return tree


# this class represents a node of the linked list at the core of the Fibonacci
#   heap; it is a wrapper for the tree that is the actual list element
# it contains the tree as well as fields to maintain the doubly linked list
# it contains methods to look at the key at the top of its tree and to merge
#   itself with another CircNode
class CircNode(object) :
    def __init__(self, tree) :
        self.tree = tree
        self.prev = None
        self.next = None

    def key() :
        return self.tree.root.key

    def merge(other_node) :
        self.tree = self.tree.merge_with(other_node.tree)


# the actual Fibonacci heap
# contains only a reference to the min CircNode in the heap
class FibHeap(object) :
    def __init__(self) :
        self.min = None

    # returns whether or not this heap is empty
    def is_empty() :
        return self.min == None

    # inserts the given CircNode into the heap ("adds a new tree")
    def insert(cnode) :
        pass

    # returns the minimum element of the heap (as a TreeNode) without
    #   removing it
    def min() :
        return self.min.tree.root

    # returns the minimum element of the heap (as a TreeNode) and removes
    #   it from the heap
    def pop() :
        pass

    # decreases the key of the given TreeNode to the specified value
    def decr_key(tnode, new_key) :
        pass

    # removes the given TreeNode from the heap (does not return the node)
    def delete(tnode) :
        pass

    # merges this heap with another Fibonacci heap
    def merge(other_heap) :
        pass

    # returns the TreeNode with the given key, or None if key not in heap
    def find(key) :
        pass

    # restructures the heap's core double-linked-list after the removal
    #   of one of the heap's elements
    def restructure() :
        pass

