from operator import attrgetter

def pq_member(prioq, url) :
    for any in prioq.queue :
        if any.self_url.lower() == url.lower() :
            return any
    return None

def pq_push(prioq, tnode) :
    prioq.put_nowait(tnode)
    prioq.queue.sort(key=attrgetter("key"))
    
def pq_pop(prioq) :
    rv = prioq.get_nowait()
    prioq.queue.sort(key=attrgetter("key"))
    return rv



"""
class TNodePriorityQueue(object) :
    def __init__(self) :
        queue = []
        qsize = 0
        empty = True

        

    def push(self, elt) :
        self.queue.append(elt)
        qsize += 1
        empty = qsize == 0
        self.queue = self.sort()
    
    def pop(self) :
        self.queue.pop(0)
        qsize -= 1
        empty = qsize == 0
        
    def sort(self) :
        h = []
        for each in self.queue :
            h.heappush(each.key)
        
        
    def index(self, key) :
    
    
    
    
def TNodeHeapSort(queue) :
    """