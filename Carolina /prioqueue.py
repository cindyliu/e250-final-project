from operator import attrgetter

# These functions add on to those currently provided by Python's
# built-in Priority Queue class

# Checks a prioqueue to see if the given url is already in that prioqueue.
def pq_member(prioq, url) :
    for any in prioq.queue :
        if any.self_url.lower() == url.lower() :
            return any
    return None

# The built-in Python Priority Queue doesn't seem to allow for sorting by
# keys within complex objects, so I reimplemented queue pushing for our use
def pq_push(prioq, tnode) :
    prioq.put_nowait(tnode)
    prioq.queue.sort(key=attrgetter("key"))

# Same; using the Priority Queue inbuilt pop method wasn't producing correct
# results and it seemed to be due to sorting inconsistencies, so I also
# redefined pop for our use
def pq_pop(prioq) :
    rv = prioq.get_nowait()
    prioq.queue.sort(key=attrgetter("key"))
    return rv
