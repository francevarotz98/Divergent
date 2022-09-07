from scapy.all import *
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import csv

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

def ex_features_from_pcap(f_pcap, port_server):
    """
    Output: file.csv which containts nested list with features
    """

    path='/home/francesco/Desktop/UniPd/thesis/master_project/out/'
    filename = f_pcap.split("/")[1] #sys.argv[1].split("/")[1]
    filename = filename[:len(filename)-5]
    ext_pcap = '.pcap'
    ext_csv  = '.csv'

    packets = rdpcap(path+filename+ext_pcap)#Lists to hold packet info

    #0- global pkt size [Byte],
    #1- pkt size of each pkt [Byte],
    #2- inter-arrival time [us],
    #3- density packets [pkt],
    #4- burst bandwidth [todo],
    #5- per-direction bandwidth  [todo]
    features=[]

    global_pkt_size = []
    pktBytes    = []
    pktTimes    = []
    inter_times = []
    times_pkt   = []
    densities   = [] #array which contains n° pkt every DENS_TIME seconds
    DENS_TIME   = 1500 #TODO: adjust the value if needed

    #useful variable for computing inter-arr time
    # between 2 pkts
    prev_pktTime = -1
    index        = 1
    start_time   = -1 #start time of interval
    end_time     = -1 #end time of interval

    #useful variables for computing how many packets
    #come every DENS_TIME seconds (density)
    num_pkt = 0

    for pkt in packets:
        if IP in pkt:
            try:

                if int(pkt[TCP].dport) == int(port_server):
                    pktBytes.append(-1*(pkt[IP].len))
                else:
                    pktBytes.append(pkt[IP].len)

                #convert Epoch time to a datetime
                pktTime = datetime.fromtimestamp(pkt.time)
                #have to take ms in this way cause
                # fromtimestamp() seems it puts
                # ms to 0
                ms = str(pkt.time).split(".")[1]
                pktTime = pktTime.strftime("%m-%d %H:%M:%S")+"."+ms
                #print("pktTime:",pktTime)
                pktTimes.append(pktTime) #pktTimes.append(str(round(float(pktTime),6)))

                #if first iteration, append 0ms to inter_times and set last_timestamp
                # to beginning of time (time does not start from 0)
                if prev_pktTime == -1:
                    prev_pktTime = float(pktTime.split(":")[2])
                    base_time = prev_pktTime
                    inter_times.append(float(0))
                    num_pkt += 1
                    start_time = float(ms)
                    end_time = start_time+(index*DENS_TIME)
                    times_pkt.append(0)
                    #print("[D] ms:",ms)
                else:
                    pktTime = float(pktTime.split(":")[2])
                    times_pkt.append(round(pktTime-base_time,5))
                    #TODO: multiply values in inter_times for 1e3 in order
                    # to not have too small values
                    inter_times.append(round(pktTime-prev_pktTime,6))
                    prev_pktTime = pktTime

                    #if we didn't go beyond the end of the time interval set by end_time,increase
                    # num_pkt variable by 1, otherwise append num_pkt to densities
                    # reset num_pkt and set end_time to the end of the next time
                    # interval
                    if float(ms) <= end_time:
                        num_pkt += 1
                    else:
                        densities.append(num_pkt)
                        #scarica tutti gli intervalli tali per cui nessun pacchetto
                        # arriva; aggiungi quindi 0 a densities
                        enter_once = 0 #flag useful for setting 0 to intervals with no packets
                        for i in range(1000):
                            if float(ms) > start_time + (index*DENS_TIME):
                                index += 1
                                if enter_once == 0:
                                    enter_once = 1
                                elif enter_once == 1:
                                    densities.append(0)
                            else:
                                break
                        enter_once = 0

                        #print("[D] ms:",ms)
                        num_pkt = 1
                        end_time = start_time + (index*DENS_TIME)
                        #print("[D] new end_time:",end_time)


            except Exception as e:
                print("[-] Exception:",e)

    #if after for loop we have counter num_pkt packets, but the time interval was
    # not ended, then append num_pkt to densities
    if num_pkt > 0:
        densities.append(num_pkt-1)


    global_pkt_size.append(sum(pktBytes))
    #since we will use a CNN model with 2D convolutional
    #   layer, we 'pad' global_pkt_size to len(pktBytes),
    #   which is equal to len(pktTimes) by construction,
    #   with 0s
    for x in range(1,len(pktTimes)):
        global_pkt_size.append(0)

    """
    #plt.plot([ (float(start_time) + (i*DENS_TIME)) for i in range(len(densities))],densities, marker="o")
    plt.scatter([ (float(start_time) + (i*DENS_TIME)) for i in range(len(densities))],densities)
    plt.xlabel('time interval')
    plt.ylabel('#pkt')
    plt.title('Density packets w/out Divergent')
    plt.show()
    """

    #pad pktBytes, pktTimes, ... to max number of packets
    # the attacker intercepts in whole traffic flows.
    #Needed for training the CNN model which needs samples with
    # same dimensions.
    #TODO: fare check che se array ha piu di MAX_PKT_TRAFFIC elements, allora
    # bisogna stoppare l'esperimento, aumentare MAX_PKT_TRAFFIC e runnare tutto da capo
    MAX_PKT_TRAFFIC = 1450 #value computed empirically. change if needed
    for x in range(1,MAX_PKT_TRAFFIC-len(global_pkt_size)):
        global_pkt_size.append(0)

    for x in range(1,MAX_PKT_TRAFFIC-len(pktBytes)):
        pktBytes.append(0)

    for x in range(1,MAX_PKT_TRAFFIC-len(inter_times)):
        inter_times.append(0)

    for x in range(1,MAX_PKT_TRAFFIC-len(densities)):
        densities.append(-1)

    for x in range(1,MAX_PKT_TRAFFIC-len(times_pkt)):
        times_pkt.append(-1)

    #set feature-arrays to have up to MAX_PKT_TRAFFIC elements
    global_pkt_size = global_pkt_size[:MAX_PKT_TRAFFIC-1]
    pktBytes = pktBytes[:MAX_PKT_TRAFFIC-1]
    inter_times = inter_times[:MAX_PKT_TRAFFIC-1]
    densities = densities[:MAX_PKT_TRAFFIC-1]

    #print(len(global_pkt_size))
    #print(len(inter_times))
    #print(len(densities))


    assert len(pktBytes) \
    == len(global_pkt_size) \
    == len(inter_times) \
    == len(densities), "[-] Length of features arrays are different"

    features.append(global_pkt_size)
    features.append(pktBytes)
    features.append(times_pkt) #features.append(inter_times)
    features.append(densities)


    print("[i] out features:"+"./features/"+filename+ext_csv)
    with open("features/"+filename+ext_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(features)



ex_features_from_pcap(sys.argv[1], sys.argv[2])
