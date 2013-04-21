from fibheap import *

def Dijkstra(G,start,end):
	dist = {}	#distances
	pred = {}	#predecessors
	heap = FibHeap()   # est.dist. of non-final vert.
	heap[start] = 0
	
	for v in heap:
		dist[v] = heap[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = dist[v] + G[v][w]
			if w in dist:
				if vwLength < dist[w]:
					raise ValueError, "Error"
			elif w not in heap or vwLength < heap[w]:
				heap[w] = vwLength
				P[w] = v
	
	return (dist,P)
			
def shortestPath(G,start,end):
	dist,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path