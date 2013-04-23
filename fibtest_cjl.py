# tests for fibheap

from fibheap_cjl import *

# ****** tests for TreeNode functions ***********
print "Testing TreeNode.add_child"
tnode1 = TreeNode(1,"some url")
tnode2 = TreeNode(2,"some url")
tnode3 = TreeNode(3,"some url")
tnode4 = TreeNode(4,"some url")
tnode5 = TreeNode(5,"some url")
tnode1.add_child(tnode2)
tnode2.add_child(tnode3)
tree1 = Tree(tnode1)
tree1.print_tree()
tnode2.add_child(tnode4)
tree1.print_tree()
tnode3.add_child(tnode5)
tree1.print_tree()

print "Testing TreeNode.cut_child"
cut_off_node = tnode2.cut_child(1)
tree2 = Tree(cut_off_node)
tree1.print_tree()
tree2.print_tree()

# ****** tests for Tree functions ***********
#TBD


# ****** tests for FibHeap functions ***********

# try to recreate the situation in the princeton notes
print "----Testing FibHeap----"
tnode7 = TreeNode(7,"url")
tnode30 = TreeNode(30,"url")
tnode7.add_child(tnode30)

tnode26 = TreeNode(26,"url")
tnode35 = TreeNode(35,"url")
tnode26.add_child(tnode35)
tnode46 = TreeNode(46,"url")
tnode24 = TreeNode(24,"url")
tnode24.add_child(tnode26)
tnode24.add_child(tnode46)

tnode23 = TreeNode(23,"url")

tnode17 = TreeNode(17,"url")

tnode3 = TreeNode(3,"url")
tnode18 = TreeNode(18,"url")
tnode39 = TreeNode(39,"url")
tnode18.add_child(tnode39)
tnode52 = TreeNode(52,"url")
tnode41 = TreeNode(41,"url")
tnode44 = TreeNode(44,"url")
tnode41.add_child(tnode44)
tnode3.add_child(tnode18)
tnode3.add_child(tnode52)
tnode3.add_child(tnode41)

fibheap = FibHeap()
fibheap.insert(tnode7)
fibheap.insert(tnode24)
fibheap.insert(tnode23)
fibheap.insert(tnode17)
fibheap.insert(tnode3)
fibheap.print_heap()


print "\n----Testing pop----"

fibheap.pop()
#min_Tree = Tree(fibheap.pop())
#min_Tree.print_tree()
fibheap.print_heap()

# test for one-node heap
fibheap1 = FibHeap()
fibheap1.insert(TreeNode(50,"url"))
fibheap1.print_heap()


print "\n----Testing decr_key----"

tnode7 = TreeNode(7,"")
tnode24 = TreeNode(24,"")
tnode17 = TreeNode(17,"")
tnode23 = TreeNode(23,"")
tnode26 = TreeNode(26,"")
tnode46 = TreeNode(46,"")
tnode30 = TreeNode(30,"")
tnode35 = TreeNode(35,"")
tnode88 = TreeNode(88,"")
tnode72 = TreeNode(72,"")
tnode18 = TreeNode(18,"")
tnode21 = TreeNode(21,"")
tnode39 = TreeNode(39,"")
tnode52 = TreeNode(52,"")
tnode38 = TreeNode(38,"")
tnode41 = TreeNode(41,"")

tnode26.add_child(tnode35)
tnode26.add_child(tnode88)
tnode46.add_child(tnode72)
tnode24.add_child(tnode26)
tnode24.add_child(tnode46)
tnode17.add_child(tnode30)
tnode21.add_child(tnode52)
tnode7.add_child(tnode24)
tnode7.add_child(tnode17)
tnode7.add_child(tnode23)
tnode18.add_child(tnode21)
tnode18.add_child(tnode39)
tnode38.add_child(tnode41)
fh = FibHeap()
fh.insert(tnode7)
fh.insert(tnode18)
fh.insert(tnode38)
fh.print_heap()

print "\n----Test case 0:"
fh.decr_key(tnode46,45)
fh.print_heap()

print "\n----Test case 1:"
fh.decr_key(tnode46,15)
fh.print_heap()

print "\n----Test case 2:"
fh.decr_key(tnode35,5)
fh.print_heap()

print "\n----Test case new-min:"
fh = FibHeap()
fh.insert(tnode7)
fh.insert(tnode18)
fh.insert(tnode38)
fh.decr_key(tnode46,0)
fh.print_heap()


print "\n----Testing delete----"
print "\n----Delete leaf:"
fh = FibHeap()
fh.insert(tnode7)
fh.insert(tnode18)
fh.insert(tnode38)
fh.delete(tnode35)
fh.print_heap()
print "\n----Delete internal:"
fh = FibHeap()
fh.insert(tnode7)
fh.insert(tnode18)
fh.insert(tnode38)
fh.delete(tnode24)
fh.print_heap()
print "\n----Delete root (not min):"
fh = FibHeap()
fh.insert(tnode7)
fh.insert(tnode18)
fh.insert(tnode38)
fh.delete(tnode18)
fh.print_heap()


print "\n----Testing merge----"
tnode7 = TreeNode(7,"url")
tnode30 = TreeNode(30,"url")
tnode7.add_child(tnode30)
tnode26 = TreeNode(26,"url")
tnode35 = TreeNode(35,"url")
tnode26.add_child(tnode35)
tnode46 = TreeNode(46,"url")
tnode24 = TreeNode(24,"url")
tnode24.add_child(tnode26)
tnode24.add_child(tnode46)
tnode23 = TreeNode(23,"url")
tnode17 = TreeNode(17,"url")
tnode3 = TreeNode(3,"url")
tnode18 = TreeNode(18,"url")
tnode39 = TreeNode(39,"url")
tnode18.add_child(tnode39)
tnode52 = TreeNode(52,"url")
tnode41 = TreeNode(41,"url")
tnode44 = TreeNode(44,"url")
tnode41.add_child(tnode44)
tnode3.add_child(tnode18)
tnode3.add_child(tnode52)
tnode3.add_child(tnode41)
fibheap = FibHeap()
fibheap.insert(tnode7)
fibheap.insert(tnode24)
fibheap.insert(tnode23)
fibheap.insert(tnode17)
fibheap.insert(tnode3)
fibheap.print_heap()

tnode7 = TreeNode(7,"")
tnode24 = TreeNode(24,"")
tnode17 = TreeNode(17,"")
tnode23 = TreeNode(23,"")
tnode26 = TreeNode(26,"")
tnode46 = TreeNode(46,"")
tnode30 = TreeNode(30,"")
tnode35 = TreeNode(35,"")
tnode88 = TreeNode(88,"")
tnode72 = TreeNode(72,"")
tnode18 = TreeNode(18,"")
tnode21 = TreeNode(21,"")
tnode39 = TreeNode(39,"")
tnode52 = TreeNode(52,"")
tnode38 = TreeNode(38,"")
tnode41 = TreeNode(41,"")
tnode26.add_child(tnode35)
tnode26.add_child(tnode88)
tnode46.add_child(tnode72)
tnode24.add_child(tnode26)
tnode24.add_child(tnode46)
tnode17.add_child(tnode30)
tnode21.add_child(tnode52)
tnode7.add_child(tnode24)
tnode7.add_child(tnode17)
tnode7.add_child(tnode23)
tnode18.add_child(tnode21)
tnode18.add_child(tnode39)
tnode38.add_child(tnode41)
fh = FibHeap()
fh.insert(tnode7)
fh.insert(tnode18)
fh.insert(tnode38)
fh.print_heap()

fibheap.merge(fh)
fibheap.print_heap()
print "\n----And reversed positions:"
tnode7 = TreeNode(7,"url")
tnode30 = TreeNode(30,"url")
tnode7.add_child(tnode30)
tnode26 = TreeNode(26,"url")
tnode35 = TreeNode(35,"url")
tnode26.add_child(tnode35)
tnode46 = TreeNode(46,"url")
tnode24 = TreeNode(24,"url")
tnode24.add_child(tnode26)
tnode24.add_child(tnode46)
tnode23 = TreeNode(23,"url")
tnode17 = TreeNode(17,"url")
tnode3 = TreeNode(3,"url")
tnode18 = TreeNode(18,"url")
tnode39 = TreeNode(39,"url")
tnode18.add_child(tnode39)
tnode52 = TreeNode(52,"url")
tnode41 = TreeNode(41,"url")
tnode44 = TreeNode(44,"url")
tnode41.add_child(tnode44)
tnode3.add_child(tnode18)
tnode3.add_child(tnode52)
tnode3.add_child(tnode41)
fibheap = FibHeap()
fibheap.insert(tnode7)
fibheap.insert(tnode24)
fibheap.insert(tnode23)
fibheap.insert(tnode17)
fibheap.insert(tnode3)

tnode7 = TreeNode(7,"")
tnode24 = TreeNode(24,"")
tnode17 = TreeNode(17,"")
tnode23 = TreeNode(23,"")
tnode26 = TreeNode(26,"")
tnode46 = TreeNode(46,"")
tnode30 = TreeNode(30,"")
tnode35 = TreeNode(35,"")
tnode88 = TreeNode(88,"")
tnode72 = TreeNode(72,"")
tnode18 = TreeNode(18,"")
tnode21 = TreeNode(21,"")
tnode39 = TreeNode(39,"")
tnode52 = TreeNode(52,"")
tnode38 = TreeNode(38,"")
tnode41 = TreeNode(41,"")
tnode26.add_child(tnode35)
tnode26.add_child(tnode88)
tnode46.add_child(tnode72)
tnode24.add_child(tnode26)
tnode24.add_child(tnode46)
tnode17.add_child(tnode30)
tnode21.add_child(tnode52)
tnode7.add_child(tnode24)
tnode7.add_child(tnode17)
tnode7.add_child(tnode23)
tnode18.add_child(tnode21)
tnode18.add_child(tnode39)
tnode38.add_child(tnode41)
fh = FibHeap()
fh.insert(tnode7)
fh.insert(tnode18)
fh.insert(tnode38)

fh.merge(fibheap)
fh.print_heap()
