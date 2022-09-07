import os

def compute_bandwidth_overhead():
    '''
    compute the bandwidth overhead introduced by
    Divergent wrt the traffic without defence.
    @arg:
    @return: band_overhead
    '''

    band_overhead     = 0
    total_size_no_def = 0
    total_size_div    = 0

    path = "/home/francesco/Desktop/UniPd/thesis/master_project/overhead/"
    path_div = "/home/francesco/Desktop/UniPd/thesis/master_project/overhead_div/"
    files = sorted(os.listdir(path))
    files_div = sorted(os.listdir(path_div))

    d = {}
    #i = 0
    #compute total size in traffic with no defence
    for file_name in files:
        #print("[D] file_name:"+file_name)
        f  = open(path+file_name,"r")
        size_no_def = int(f.read().splitlines()[0].split(",")[0])

        if not file_name[24:] in d:
            d[file_name[24:]] = [size_no_def]
        else:
            d[file_name[24:]].append(size_no_def)

        #print("[D] size_no_def:",size_no_def)
        total_size_no_def += size_no_def
        f.close()

        #i+=1
        #if i == 10:
        #    break

    #print("-"*80)
    #i=0

    #compute total size in traffic with Divergent
    for file_name in files_div:
        #print("[D] file_name:"+file_name)
        f  = open(path_div+file_name,"r")
        size_div = int(f.read().splitlines()[0].split(",")[0])

        if not file_name[24:] in d:
            d[file_name[24:]] = [size_div]
        else:
            d[file_name[24:]].append(size_div)

        #print("[D] size_div:",size_div)
        total_size_div += size_div
        f.close()

        #i+=1
        #if i == 10:
        #    break

    #print(d)
    #for key, value in d.items():
        #print(f"Overhead {key}: {(1-value[0]/value[1])*100}%")

    band_overhead = total_size_no_def/total_size_div
    return band_overhead

if __name__ == "__main__":
    b_over = compute_bandwidth_overhead()
    print("[+] Bandwidth overhead introduced: {:.2f}%".format((1-b_over)*100))
