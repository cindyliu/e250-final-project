# tests for fibheap

from fibheap_yjp import *
"""
# ****** tests for TreeNode functions ***********
# test for add_child
tnode1 = TreeNode(1,"some url")
tree1 = Tree(tnode1)

tnode2 = TreeNode(2,"some url")
tnode1.add_child(tnode2)

tnode3 = TreeNode(3,"some url")
tnode2.add_child(tnode3)

#print
#tree1.print_tree()

tnode4 = TreeNode(4,"some url")
tnode2.add_child(tnode4)

#print
#tree1.print_tree()

tnode5 = TreeNode(5,"some url")
tnode3.add_child(tnode5)

#print
tree1.print_tree()

# test for cut_child
cut_off_node = tnode2.cut_child(1)
tree2 = Tree(cut_off_node)
tree1.print_tree()
tree2.print_tree()

# ****** tests for Tree functions ***********
#TBD
"""

# ****** tests for FibHeap functions ***********

# *** pop() ***
# try to recreate the situation in the princeton notes
tnode7 = TreeNode(7,"url")
tnode30 = TreeNode(30,"url")
tnode24 = TreeNode(24,"url")
tnode26 = TreeNode(26,"url")
tnode35 = TreeNode(35,"url")
tnode46 = TreeNode(46,"url")
tnode23 = TreeNode(23,"url")
tnode17 = TreeNode(17,"url")
tnode3 = TreeNode(3,"url")
tnode18 = TreeNode(18,"url")
tnode39 = TreeNode(39,"url")
tnode52 = TreeNode(52,"url")
tnode41 = TreeNode(41,"url")
tnode44 = TreeNode(44,"url")

circnode7 = CircNode(Tree(tnode7))
circnode7.merge(CircNode(Tree(tnode30)))
fibheap = FibHeap()
fibheap.insert(circnode7)

circnode24 = CircNode(Tree(tnode24))
circnode24.merge(CircNode(Tree(tnode26)))
tnode26.add_child(tnode35)
circnode24.merge(CircNode(Tree(tnode46)))
fibheap.insert(circnode24)

circnode23 = CircNode(Tree(tnode23))
fibheap.insert(circnode23)

circnode17 = CircNode(Tree(tnode17))
fibheap.insert(circnode17)

circnode3 = CircNode(Tree(tnode3))
tnode3.add_child(tnode18)
tnode3.add_child(tnode52)
tnode3.add_child(tnode41)
tnode18.add_child(tnode39)
tnode41.add_child(tnode44)
fibheap.insert(circnode3)

fibheap.print_heap()

print "\nthis is after pop"
fibheap.pop()
fibheap.print_heap()

# test for one-node heap
print "\n this is test of pop for one-node (key 50) FibHeap"
fibheap1 = FibHeap()
fibheap1.insert(CircNode(Tree(TreeNode(50,"url"))))
pop_result = fibheap1.pop()
print repr(pop_result.key)
print ("remaining tree is empty:" + repr(fibheap1.is_empty()))

# *** find ***
print "\n this is test of find"
print "this is the FibHeap we search"
temp_answer_tnode = fibheap.find(7)
print "find 7 (at root):" + repr(temp_answer_tnode.key)
temp_answer_tnode = fibheap.find(35)
print "find 35 (child of child):" + repr(temp_answer_tnode.key)
temp_answer_tnode = fibheap.find(51)
print "find 51 (doesn't exist):" + repr(temp_answer_tnode)
