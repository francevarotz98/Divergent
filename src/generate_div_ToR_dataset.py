import os
import numpy as np


def generate_div_ToR_dataset(path, dict_cluster):
    """
    Starting from dataset created by Wang T., create a dataset with the same
    data-cells, but with Divergent defence in place.

    @args: path: path to cell-files
           dict_cluster: dictionary which contains as key
            the number of cluster and as values the sizes of the files

    @return: 0
    """
    #THRESHOLD_FILE_SIZE = 28019  # threshold for size of files requested, which
    #  define which binomial distribution to use for
    #  generating SECRET_NUMBER
    SECRET_NUMBER = 0

    path_div = "/home/francesco/Desktop/UniPd/thesis/dataset_sota_small_div/"
    if not os.path.isdir(path_div):
        os.mkdir(path_div)

    cells = os.listdir(path)

    for cell_name in cells:
        print("[D] cell_name:"+cell_name)
        if cell_name == ".README.txt":
            break
        cell_file = open(path+cell_name, "r")
        cell_values = cell_file.read().splitlines()
        byte_size = os.stat(path+cell_name).st_size
        while SECRET_NUMBER == 0:
            # draw SECRET_NUMBER from binomial distribution which depends
            # on the size of the file.
            num_cluster = search_cluster(dict_cluster, byte_size)
            print("byte_size:",byte_size)

            #assert num_cluster >= 0, "[-] Cluster not found ..."
            print("num_cluster:", num_cluster)
            # if cell belongs to resource 4 (the smallest one), assign
            # a specific binomial distribution
            if int(cell_name[0]) == 4:
                SECRET_NUMBER = np.random.binomial(n=4, p=0.5)
            else:
                # after 5 clusters, increase the n parameter by one.
                # NOTE: num_cluster depends on the size of the file: the bigger
                #    it is, the bigger num_cluster will be, the bigger the n
                #    parameter of the binomial  distribution will be employed.
                SECRET_NUMBER = np.random.binomial(n=int(6+0.2*num_cluster), p=0.5)

        # index_random_dum used to count when sending dummy pkt
        index_random_dum = 0
        if num_cluster >=0:
            out_div_file = open(path_div+cell_name+"_div", "w")
        for i in range(len(cell_values)):
            if num_cluster == -1:
                print("[-] Cluster not found ...")
                break
            # if I enter in the if, then real packet sent
            if index_random_dum < SECRET_NUMBER:
                index_random_dum += 1
                out_div_file.write(cell_values[i]+"\n")
            # else, send burst of dummy packets
            else:
                # num_burst represents how many consecutive
                # dummy packets we send
                if int(cell_name[0]) == 4:
                    num_burst = np.random.binomial(n=16, p=0.5)
                else:
                    num_burst = np.random.binomial(n=8, p=0.5)
                # print("[D] num_burst:",num_burst)
                time_next_real_cell = float(cell_values[i].split()[0])
                time_prev_real_cell = float(cell_values[i-1].split()[0])
                # inc_time_dummy_cell measures the increment of time to add
                # to each cell
                if num_burst > 0:
                    inc_time_dummy_cell = (time_next_real_cell-time_prev_real_cell)/num_burst
                for k in range(num_burst):
                    # i'm writing the time of the dummy packet, a tab, number 1 in str and newline
                    out_div_file.write(str(round(time_prev_real_cell+(k+1)*inc_time_dummy_cell, 4))+"\t"+"1"+"\n")

                # at the end of having written burst of dummies,
                # write also real value, otherwise it
                # will be lost due to next iteration
                out_div_file.write(cell_values[i]+"\n")
                index_random_dum = 0

        # reset SECRET_NUMBER to 0
        SECRET_NUMBER = 0
        cell_file.close()
        if num_cluster >= 0:
            out_div_file.close()
        print("-"*80)


    return 0


def generate_clusters(path):
    """
    Generate clusters based on size of resource.

    @arg: path
    @return: dict_cluster
    """
    cells = os.listdir(path)
    sizes = []

    for cell_name in cells:
        byte_size = os.stat(path+cell_name).st_size
        #print("[D] cell_name:"+cell_name+f":{byte_size}")
        sizes.append(int(byte_size))

    sizes.sort()

    # smaller resources will be assigned to smaller
    #  cluster number and viceversa
    dict_cluster = {}
    index_cluster = 0  # index of the cluster to be assigned to
    elements_in_cluster = 20  # how many elements per cluster
    el_in_cluster = 0
    for size in sizes:
        if el_in_cluster < elements_in_cluster:
            if index_cluster in dict_cluster:
                dict_cluster[index_cluster].append(size)
            else:
                dict_cluster[index_cluster] = [size]
            el_in_cluster += 1

        else:
            index_cluster += 1
            el_in_cluster = 0

    for k, v in dict_cluster.items():
        print(k, ":", v)

    return dict_cluster


def search_cluster(dict_cluster, size):
    """
    Look for cluster of file of dimension 'size', given dict_cluster.

    @return: -1: cluster not found
    """
    num_cluster = -1
    for key in dict_cluster:
        for i in range(len(dict_cluster[key])):
            if dict_cluster[key][i] == size:
                num_cluster = key
                break
        if num_cluster != -1:
            break

    return num_cluster


if __name__ == "__main__":
    dict_cluster = generate_clusters("/home/francesco/Desktop/UniPd/thesis/dataset_sota_small/")
    generate_div_ToR_dataset("/home/francesco/Desktop/UniPd/thesis/dataset_sota_small/", dict_cluster)
