# this is the front end for connecting-urls program
from dijkstra_yjp_20130429_wiki import * 
from dijkstra_prioqueue_wiki import *
from dijkstra_binheap_wiki import *
from dict_operations_wiki import *

# main command-line options:
# -d => specify the depth to crawl; default is 30
# -t => specify which priority structure to use for Dijkstra's;
#		default is "fibheap", other options are "heapq" and "prioqueue"
def main():
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth = opts.depth
    qtype = opts.type

    start_time = dict_time = time.clock()
    dict = {}

    output_for_destination_urls = open("options_for_destination_urls.txt", "w+")     
    output_f = open("output_for_debugging.txt", "w+") 

    if opts.from_file :
        dict = build_dict(dictfilename)
        if len(dict) == 0 :
            print >> sys.stderr, "Error: empty dictionary"
            exit(1)
        dict_time = time.clock() - start_time
        print "Finished building dict from file: took %gms" % (1000*dict_time)
        write_dict(dict, "File_Dict_Output-" + qtype + ".txt") 
    else :   
        print "Crawling %s (Max Depth: %d)" % (url, depth)
        crawler = Crawler(url, depth)
        crawler.crawl()
        dict = crawler.urls
        dict_time = time.clock() - start_time
        print "Got dict from crawler: crawling took %gms" % (1000*dict_time)
        write_dict(dict, "Crawled_Dict_Output.txt") 

#create fibheap/Dijkstra's graph with the urls found
    if qtype == "fibheap" :
        (fibheap,urlset) = from_dict_to_fibheap_urlset(dict, url, output_f)
        print "Making Fibheap took %gms" %(1000*(time.clock() - start_time - dict_time))
        print "size of set %d" %(len(urlset))
    elif qtype == "binheap" :
        (bheap,urlset) = from_dict_to_binheap_urlset(dict, url)
        print "Making Binheap took %gms" % (1000*(time.clock() - start_time - dict_time))
        print "size of set %d" %(len(urlset))
    elif qtype == "prioqueue" :
        (prioq,urlset) = from_dict_to_prioqueue_urlset(dict, url)
        print "Making PrioQueue took %gms" %(1000*(time.clock() - start_time - dict_time))
        print "size of urlset %d" % len(urlset)
    else :
        print "Please specify one of the following priority structures:"
        print "\t  fibheap - Fibonacci Heap"
        print "\t  binheap - min-priority binary heap (array implemented)"
        print "\tprioqueue - priority queue"
        sys.exit(1)
    
    # should write a numbered list of potential destination urls to a list
    # and the list writes to options_for_destination_urls.txt

    start_time = time.clock()
    i = 0
    list_of_urls = []
    for elt in urlset:
        list_of_urls.append(elt)
        print >> output_for_destination_urls, repr(i) + " " + repr(elt)
        i = i+1
    output_for_destination_urls.close()
    print "Getting destination urls took %gms" % (1000*(time.clock() - start_time))
        
    # should ask user to input a number matching of these potential destination urls
    # and reject that are <0 or > len of the list    
    index_dest_url = raw_input("Enter the number corresponding to the destination url you wish to connect to: ")
    while int(float(index_dest_url)) < 0 or int(float(index_dest_url)) > len(list_of_urls) - 1:
        index_dest_url = raw_input("Number is too big or too small. Please enter an integer corresponding to the destination url you wish to connect to, that is listed in options_for_destination_urls.txt")
    print "The destination url you selected is " + list_of_urls[int(float(index_dest_url))]
    
    start_time = time.clock()
    
    if qtype == "fibheap" :
#        print >> output_f, "\n this is the min of the heap" + fibheap.min.tree.root.self_url
        findShortestPath(fibheap, list_of_urls[int(float(index_dest_url))], output_f)
    elif qtype == "prioqueue" :
        findShortestPath_PQ(prioq, list_of_urls[int(float(index_dest_url))])
    elif qtype == "binheap" :
        findShortestPath_BH(bheap, list_of_urls[int(float(index_dest_url))])
    else :
        print >> sys.stderr, "Error: invalid priority structure given"
        sys.exit(1)
    
    print "Dijkstra's took %gms." % (1000*(time.clock() - start_time))
    
if __name__ == "__main__":
    main()