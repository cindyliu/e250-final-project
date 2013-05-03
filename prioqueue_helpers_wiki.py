def pq_member(self, url) :
    for any in self.queue :
        if any.self_url.lower() == url.lower() :
            return True
    return False



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