# this is the front end for connecting-urls program
from graph import *
from dijkstra import *

# main command-line options:
# -d => specify the depth to crawl; default is 30
# -t => specify which priority structure to use for Dijkstra's;
#		default is "fibheap", the other option is "prioqueue"
# -f => instead of recrawling all pages, read from dict file

def main():

    #Parsing out input arguments
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0
      
    depth = opts.depth
    qtype = opts.type
    dict_from_file = opts.from_file
    
    #Checking valid input arguments
    if (not (qtype == 'fibheap')) and (not (qtype == 'prioqueue')) :
        print "Please specify one of the following priority structures:"
        print "\t  fibheap - Fibonacci Heap"
        print "\t prioqueue - priority queue"
        sys.exit(1)

	#Starting timer
    start_time = dict_time = time.clock()
    
    #dict = {}
    
    #Creating output files 
    output_for_destination_urls = open("options_for_destination_urls.txt", "w+")  
    output_f = open("output_for_debugging.txt", "w+")
    stats = open("stats.txt", "a+")
    
    #Checking if dictionary has been created, and "read_from_dict" option given
    if dict_from_file :
        print >> stats, qtype, "file", depth
        dict = build_dict(dictfilename)
        if len(dict) == 0 :
            print >> sys.stderr, "Error: empty dictionary"
            sys.exit(1)
        dict_time = time.clock() - start_time
        print "Finished building dict from file: took %gms" % (1000*dict_time)
    else :
        print >> stats, qtype, "crawled", depth
        print "Crawling %s (Max Depth: %d)" % (url, depth)
        crawler = Crawler(url, depth)
        crawler.crawl()
        dict = crawler.urls
        dict_time = time.clock() - start_time
        print "Got dict from crawler: crawling took %gms" % (1000*dict_time)
    print >> stats, "dict %g" % (1000*dict_time)
        
    #Creating graph for visualization from dict
    G = dict_2_graph(dict,url)
    
    #create fibheap or priority queue from the urls found
    start_time = time.clock()

    if qtype == "fibheap" :
        (fibheap,urlset) = from_dict_to_fibheap_urlset(dict, url, output_f)
        run_time = 1000*(time.clock() - start_time)
        print "Making Fibheap took %gms" % run_time
        print "size of set %d" %(len(urlset))

    elif qtype == "prioqueue" :
        (prioq,urlset) = from_dict_to_prioqueue_urlset(dict, url)
        run_time = 1000*(time.clock() - start_time)
        print "Making PrioQueue took %gms" % run_time
        print "size of set %d" % len(urlset)
    print >> stats, "make %g" % run_time
        
    # should write a numbered list of potential destination urls to a list
    # and the list writes to options_for_destination_urls.txt
    i = 0
    list_of_urls = []
    for elt in urlset:
        list_of_urls.append(elt)
        print >> output_for_destination_urls, "\n" + repr(i) + " " + repr(elt)
        i = i+1
    output_for_destination_urls.close()
    
    json.dump(list(urlset), open('web_page/link_options.json','w'))

    # open URL in  web browser
    #http_server.load_url('web_page/link_options.html')
    
        
    # should ask user to input a number matching of these potential destination urls
    # and reject those that are <0 or > len of the list    
    index_dest_url = raw_input("Enter the number corresponding to the " +
                               "destination url you wish to connect to: ")
    while int(float(index_dest_url)) < 0 or int(float(index_dest_url)) > len(list_of_urls) - 1:
        index_dest_url = raw_input("Number is too big or too small." +
            " Please enter an integer corresponding to the destination url" +
            " you wish to connect to, that is listed in" +
            " options_for_destination_urls.txt")
    print "The destination url you selected is %s" % (
        list_of_urls[int(float(index_dest_url))])
    
    
    start_time = time.clock()
    
    if qtype == "fibheap" :
        print >> output_f, "\nthis is the min of the heap %s" % ( 
            fibheap.min.tree.root.self_url)
        (G,dij_path) = findShortestPath(fibheap, 
            list_of_urls[int(float(index_dest_url))], output_f,G)
    elif qtype == "prioqueue":
         (G,dij_path) =findShortestPath_PQ(prioq, 
             list_of_urls[int(float(index_dest_url))], G)
    
    run_time = 1000*(time.clock() - start_time)
    print "Dijkstra's took %gms." % run_time
    print >> stats, "dijk %g" % run_time
    
    stats.close()
    output_for_destination_urls.close()
    output_f.close()
    
    #Outputting graph info to JSON formated file for visualization 
    d = json_graph.node_link_data(G) # node-link format to serialize
    
    #Exporting JSON Files for js function in webpage 
    json.dump(d, open('web_page/links.json','w'))
    json.dump(dij_path, open('web_page/dij_path.json','w'))

    # open URL in  web browser
    http_server.load_url('web_page/site_map.html')
    
    
if __name__ == "__main__":
    main()
