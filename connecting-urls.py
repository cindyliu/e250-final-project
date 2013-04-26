# this is the front end for connecting-urls program
from dijkstra_yjp_20130424 import * 

def main():
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth = opts.depth

    sTime = time.time()
	
    output_for_destination_urls = open("options_for_destination_urls.txt", "w+")    
    output_f = open("output_for_debugging.txt", "w+") 
    print "Crawling %s (Max Depth: %d)" % (url, depth)
    crawler = Crawler(url, depth)
    crawler.crawl()
    dict = crawler.urls
    # should write a numbered list of potential destination urls to a list
    # and the list writes to options_for_destination_urls.txt
    list_form_of_dict = []
    for dict_key in dict:
        list_form_of_dict.append(dict_key)
        for dict_val in dict[dict_key]:
            list_form_of_dict.append(dict_val)
    
    i = 0
    for elt in list_form_of_dict:
        print >> output_for_destination_urls, "\n" + repr(i) + " " + repr(elt)
        i = i+1
    # should ask user to input a number matching of these potential destination urls
    # and reject that are <0 or > len of the list    
    index_dest_url = raw_input("Enter the number corresponding to the destination url you wish to connect to: ")
    while int(float(index_dest_url)) < 0 or int(float(index_dest_url)) > len(list_form_of_dict) - 1:
        index_dest_url = raw_input("Number is too big or too small. Please enter an integer corresponding to the destination url you wish to connect to, that is listed in options_for_destination_urls.txt")
    print "The destination url you selected is " + list_form_of_dict[int(float(index_dest_url))]
    
    #create fibheap/Dijkstra's graph with the urls found
    fibheap = from_dict_to_fibheap(dict, url, output_f)
    #fibheap.print_heap(output_f)
    print >> output_f, "\n this is the min of the heap" + fibheap.min.tree.root.self_url
    
    findShortestPath(fibheap,list_form_of_dict[int(float(index_dest_url))],output_f)
    
if __name__ == "__main__":
    main()