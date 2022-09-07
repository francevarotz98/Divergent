import os
import csv
import numpy as np

"""
features:
    0- global pkt size
    1- pkt size of each pkt
    2- inter-arrival time
    3- density packets
    4- burst bandwidth
    5- per-direction bandwidth

"""

"""
NOTE:
once the features are saved in csv file, in order to load them remember that each list is
separated by newline, while each element inside the same list is separatd by ','
"""

def add_divergent_to_data(path, dict_cluster):
    """
    Add Divergent defence to normal traffic.
    Output: file.csv which containts data with Divergent
    """

    filenames = os.listdir(path)
    ext_csv   = '.csv'
    num_clusters = max(list(dict_cluster.keys())) #total number of clusters generated
    overall_mean = get_overall_mean_cluster(dict_cluster) #mean of all the resources in the server

    MTU = 65536-20-20  # remove IP and TCP headers
    MAX_PKT_TRAFFIC = 2500
    num_file = 0
    for filename in filenames:
        features  = []
        global_pkt_size = []
        pktBytes        = []
        times           = [] #timestamp of each packet
        densities       = []
        SECRET_NUMBER   = 0
        print("Video:"+filename.split(":")[2][2:9])
        print("[D] filename:"+filename)
        file_old = open(path+filename, "r")
        file_old_values = file_old.read().splitlines()

        for i in range(len(file_old_values)):
            if i == 0:
                global_pkt_size = file_old_values[i].split(",")
            if i == 1:
                pktBytes = file_old_values[i].split(",")
            if i == 2:
                times = file_old_values[i].split(",")
            if i == 3:
                densities = file_old_values[i].split(",")

        while SECRET_NUMBER == 0:
            # draw SECRET_NUMBER from binomial distribution which depends
            # on the size of the file.
            # If video is 09 (the smallest one) or 06 (bigest one), assign
            # a specific binomial distribution
            '''
            if filename.split(":")[2][2:9] == "Video09":
                print("[D] Video09 GOT IT")
                SECRET_NUMBER = np.random.binomial(n=3, p=0.5)
            elif filename.split(":")[2][2:9] == "Video06":
                print("[D] Video06 GOT IT")
                SECRET_NUMBER = np.random.binomial(n=73, p=0.5)
            else:
                num_cluster = search_cluster(dict_cluster, filename.split(":")[2][2:9])
                # NOTE: num_cluster depends on the size of the file: the bigger
                #    it is, the bigger num_cluster will be, the bigger the n
                #    parameter of the binomial  distribution will be employed.
                mean_cluster = get_mean_cluster(dict_cluster, num_cluster)
                print("mean_cluster:",mean_cluster)
                SECRET_NUMBER = np.random.binomial(n=int(6+2*(1.2*((num_cluster)**2)/num_clusters)), p=0.5)
                print("num_cluster:",num_cluster)
            '''
            num_cluster = search_cluster(dict_cluster, filename.split(":")[2][2:9])
            print("num_cluster:",num_cluster)
            mean_cluster  = get_mean_cluster(dict_cluster, num_cluster)
            #std_cluster   = get_std_cluster(dict_cluster, num_cluster, mean_cluster)
            video_MB_size = get_size_video(dict_cluster, num_cluster, filename.split(":")[2][2:9])
            #formula to get n of Binomial depends on:
            #   > size of the resource
            #   > mean of the cluster
            #   > mean of all the resources
            #TODO: divide functions in two situations: if resource is greater
            # than the mean, than use exponential, otherwise use gauss bell,
            # with peak on the mean
            #n_bin = int(2+1.1*(np.exp(video_MB_size-mean_cluster+0.01))) #int( mean_cluster*(np.exp(-(video_MB_size - mean_cluster)**2 / (2 * std_cluster**2))))
            #if n_bin > 45:
            #    n_bin = 30
            print("mean_cluster:",mean_cluster)
            #print("std_cluster:",std_cluster)
            print("video_MB_size:",video_MB_size)
            print("overall_mean:",overall_mean)
            #print("(video_MB_size-mean_cluster)**2:",(video_MB_size-mean_cluster)**2)
            #print("0.3*(abs(video_MB_size-overall_mean)):",0.3*(abs(video_MB_size-overall_mean)))
            #print("(0.3/k)*(abs(video_MB_size-overall_mean)):",(0.3/k)*(abs(video_MB_size-overall_mean)))
            #print("n_bin:",n_bin)
            ##### cluster 2 ####
            if filename.split(":")[2][2:9] == "Video06":
                SECRET_NUMBER = np.random.binomial(n=13*2, p=0.5)
                '''
                if numpy.random.rand() > 0.5:
                    SECRET_NUMBER = np.random.binomial(n=13*2, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=13*2, p=0.5)
                '''

            elif filename.split(":")[2][2:9] == "Video07":
                if np.random.rand() > 0.5:
                    SECRET_NUMBER = np.random.binomial(n=13*2, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=16, p=0.5)

            ##### cluster 0 ####
            elif filename.split(":")[2][2:9] == "Video01":
                if np.random.rand() > 0.5:
                    SECRET_NUMBER = np.random.binomial(n=18, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=18/2, p=0.5)

            elif filename.split(":")[2][2:9] == "Video02":
                if np.random.rand() > 0.5:
                    SECRET_NUMBER = np.random.binomial(n=16, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=16/2, p=0.5)

            elif filename.split(":")[2][2:9] == "Video03":
                if np.random.rand() > 0.7:
                    SECRET_NUMBER = np.random.binomial(n=16, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=16/2, p=0.5)

            elif filename.split(":")[2][2:9] == "Video09":
                if np.random.rand() > 0.5:
                    SECRET_NUMBER = np.random.binomial(n=6, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=6/2, p=0.5)

            #### cluster 1 ####
            elif filename.split(":")[2][2:9] == "Video04":
                if np.random.rand() > 0.5:
                    SECRET_NUMBER = np.random.binomial(n=27, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=5, p=0.5)

            elif filename.split(":")[2][2:9] == "Video05":
                if np.random.rand() > 0.6:
                    SECRET_NUMBER = np.random.binomial(n=26, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=26/2, p=0.5)

            elif filename.split(":")[2][2:9] == "Video10":
                if np.random.rand() > 0.7:
                    SECRET_NUMBER = np.random.binomial(n=18, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=18/2, p=0.5)

            elif filename.split(":")[2][2:9] == "Video11":
                if np.random.rand() > 0.8:
                    SECRET_NUMBER = np.random.binomial(n=36, p=0.5)
                else:
                    SECRET_NUMBER = np.random.binomial(n=6, p=0.5)

            print("[D] SECRET_NUMBER:",SECRET_NUMBER)

        new_pktBytes  = []
        new_times     = []

        index_random_dum = 0 # used to count when sending dummy pkt
        index_pad = get_index_pad(times)

        #NOTE: all arrays global_pkt_size, pktBytes, times and densities
        # have the same length.
        # What we need to change for applying Divergent:
        #   > global_pkt_size : add MTU inserted by dummy packets
        #   > pktBytes : add bytes of dummy packets
        #   > times : add timestamps of dummy packets
        #   > densities : count dummies in densities
        for i in range(len(global_pkt_size)):
            if num_cluster == -1:
                print(f"[-] Cluster not found for {filename} ...")
                break
            # if I enter in the if, then real packet sent
            if (index_random_dum < SECRET_NUMBER) or (i>= index_pad):
                index_random_dum += 1
                new_pktBytes.append(pktBytes[i])
                new_times.append(times[i])

            # else, send burst of dummy packets (if not in 'dummy zone')
            elif i < index_pad:
                # num_burst represents how many consecutive
                # dummy packets we send
                if filename.split(":")[2][2:9] == "Video09":
                    num_burst = np.random.binomial(n=18, p=0.5)
                elif filename.split(":")[2][2:9] == "Video06":
                    num_burst = np.random.binomial(n=4, p=0.5)
                else:

                    n_bin = (20-SECRET_NUMBER) if (20-SECRET_NUMBER) > 0 else 2  #int(30-(abs(video_MB_size-mean_cluster)**2)-0.3*(abs(video_MB_size-overall_mean)))
                    #n_bin = int(15-2*(1.2*((num_cluster)**2)/num_clusters)) if int(15-2*(1.2*((num_cluster)**2)/num_clusters)) > 4 else 6
                    num_burst = np.random.binomial(n=n_bin, p=0.5)
                #print("[D] num_burst:",num_burst)
                for k in range(num_burst):
                    #create fake MTU dummy packet
                    for z in range(100):
                        mtu_dummy = np.random.binomial(n=MTU*2, p=0.5)
                        if mtu_dummy < MTU:
                            break

                    global_pkt_size[0] = int(global_pkt_size[0])+mtu_dummy
                    new_pktBytes.append(mtu_dummy)

                    time_next_real_cell = float(times[i])
                    time_prev_real_cell = float(times[i-1])
                    # inc_time_dummy_cell measures the increment of time to add
                    # to each cell
                    if num_burst > 0:
                        inc_time_dummy_cell = (time_next_real_cell-time_prev_real_cell)/num_burst
                    new_times.append(str(round(time_prev_real_cell+(k+1)*inc_time_dummy_cell, 5)))
                    #densities[TODO] += 1

                index_random_dum = 0


        new_densities = get_densities(new_times,len(new_times))

        ## pad in order to have all data with same dimensions
        for x in range(1,MAX_PKT_TRAFFIC-len(global_pkt_size)):
            global_pkt_size.append(0)

        for x in range(1,MAX_PKT_TRAFFIC-len(new_pktBytes)):
            new_pktBytes.append(0)

        for x in range(1,MAX_PKT_TRAFFIC-len(new_times)):
            new_times.append(-1)

        for x in range(1,MAX_PKT_TRAFFIC-len(new_densities)):
            new_densities.append(-1)

        #print(len(global_pkt_size))
        #print(len(new_densities))
        #print(len(new_times))
        #print(len(new_pktBytes))

        features.append(global_pkt_size)
        features.append(new_pktBytes)
        features.append(new_times)
        features.append(new_densities)

        print("[i] out features:"+"./new_features_div/"+filename)
        with open("new_features_div/"+filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(features)

        file_old.close()
        num_file += 1
        print("-"*90)
        if num_file == 900:
            break

def generate_clusters(path):
    """
    Generate clusters based on size of resources.

    @arg: path
    @return: dict_cluster
    """

    '''
    resources = os.listdir(path)
    sizes = []

    for cell_name in resources:
        byte_size = os.stat(path+cell_name).st_size
        #print("[D] cell_name:"+cell_name+f":{byte_size}")
        sizes.append(int(byte_size))

    sizes.sort()
    # smaller resources will be assigned to smaller
    #  cluster number and viceversa
    dict_cluster = {}
    index_cluster = 0  # index of the cluster to be assigned to
    elements_in_cluster = 2  # how many elements per cluster
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
            dict_cluster[index_cluster] = [size]
            el_in_cluster = 1
    '''
    #sizes are expressed in MB
    dict_cluster = {0:[("Video09", 3.894 ),("Video03", 5.720 ),("Video02", 6.873 ),("Video01", 7.531 )],
     1:[("Video05", 11.189 ),("Video10", 12.081 ),("Video11", 13.391 ),("Video04", 17.221 )],
     2:[("Video07", 21.786 ), ("Video06", 31.018 )]}
    for k, v in dict_cluster.items():
        print(k, ":", v)
        print(v[0])

    return dict_cluster


def search_cluster(dict_cluster, video_name):
    """
    Look for cluster of file of name 'video_name', given dict_cluster.

    @return: -1: cluster not found
    """
    num_cluster = -1
    for key in dict_cluster:
        for i in range(len(dict_cluster[key])):
            if dict_cluster[key][i][0] == video_name:
                num_cluster = key
                break
        if num_cluster != -1:
            break

    return num_cluster


def get_index_pad(times):
    for i in range(len(times)):
        if float(times[i]) == -1:
            return i
    return len(times)


def get_densities(times,len_pad):
    densities    = []
    DENS_TIME    = 0.000150 #NOTE: adjust the value if needed
    start_time   = -1   #start time of interval
    end_time     = -1   #end time of interval
    index        = 1
    first_time = -1
    num_pkt    = 0
    for time in times:
        if first_time == -1:
            num_pkt += 1
            start_time = float(time)
            end_time = start_time+(index*DENS_TIME)
            first_time = 1
        else:
            if float(time) <= end_time:
                num_pkt+=1
            else:
                densities.append(num_pkt)
                #scarica tutti gli intervalli tali per cui nessun pacchetto
                # arriva; aggiungi quindi 0 a densities
                enter_once = 0 #flag useful for setting 0 to intervals with no packets
                for i in range(1000):
                    if float(time) > start_time + (index*DENS_TIME):
                        index += 1
                        if enter_once == 0:
                            enter_once = 1
                        elif enter_once == 1:
                            densities.append(0)
                    else:
                        break
                enter_once = 0

                num_pkt = 1
                #tmp = end_time
                end_time = start_time + (index*DENS_TIME)
                #start_time = tmp

    for x in range(0,len_pad-len(densities)):
        densities.append(-1)

    return densities


def get_mean_cluster(dict_cluster, num_cluster):
    val_cluster = dict_cluster[num_cluster]
    sum_cl = 0
    for val in val_cluster:
        sum_cl += val[1]
    return sum_cl/len(val_cluster)


def get_std_cluster(dict_cluster, num_cluster, mean):
    val_cluster = dict_cluster[num_cluster]
    sum_num = 0
    for val in val_cluster:
        sum_num += (val[1] - mean )**2
    return np.sqrt(sum_num/(len(val_cluster)-1))

def get_overall_mean_cluster(dict_cluster):
    sum_cl = 0
    el = 0
    for k in dict_cluster:
        for val in dict_cluster[k]:
            sum_cl += val[1]
            el += 1
    return sum_cl/el


def get_size_video(dict_cluster, num_cluster, filename):
    vals = dict_cluster[num_cluster]
    for val in vals:
        if val[0] == filename:
            return val[1] #/1e6
    return -1



if __name__ == "__main__":
    path_videos = "/home/francesco/Desktop/UniPd/thesis/master_project/videos/"
    dict_cluster = generate_clusters(path_videos)
    path_featuers = "/home/francesco/Desktop/UniPd/thesis/master_project/features/"
    add_divergent_to_data(path_featuers,dict_cluster)
