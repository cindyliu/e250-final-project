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


def bh_member(bheap, url) :
    for any in bheap :
        if any.self_url.lower() == url.lower() :
            return any
    return None

def bh_empty(bheap) :
    return len(bheap) == 0
