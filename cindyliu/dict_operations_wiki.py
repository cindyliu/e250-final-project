from simple_crawler_modified_wiki import *

def build_dict(filename) :
#    print "beginning of build_dict; opening " + filename
    dictfile = open(filename, 'r')
#    print "just opened " + dictfile.name
#    print "mode is " + dictfile.mode
    curr_key = curr_val = ''
    dict = {}
    new_key = False
    if dictfile == None :
        print "Could not open file."
    else :
        dictfile.seek(0)

    print "Reading file '%s'...." % dictfile.name

    for line in dictfile :
        line = line.split(' ')
        if len(line) > 2 :
            print >> sys.stderr, "Error: whitespace in URL from file\n"
            exit(1)

        if line[0] == "key" :
            curr_key = line[1].rstrip('\n')
            new_key = True
        elif line[0] == "val" :
            curr_val = line[1].rstrip('\n')
        else :
            print >> sys.stderr, "Error: invalid line read from file\n"
            exit(1)

        if (curr_val != '') and (curr_key == '') :
            print >> sys.stderr, "Error: read value from file with no key\n"
            exit(1)

        if new_key :
            dict[curr_key] = []
        elif curr_val != curr_key :
            dict[curr_key].append(curr_val)

        new_key = False
        
#    print "Reached end of file."
    
    dictfile.close()
    return dict


def write_dict(dict,filename) :
    iter = dict.iteritems()
    dictfile = open(filename,'w+')
    
    while True :
        try :
            key, vals = iter.next()
            dictfile.write(key_prefix + key + '\n')
            for val in vals :
                dictfile.write(val_prefix + val + '\n')
        except StopIteration :
            break
    
    dictfile.close()
