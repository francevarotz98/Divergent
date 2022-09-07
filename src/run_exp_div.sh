#!/bin/bash

#pgrep tcpdump
#sudo killall tcpdump


PORT=4447

#echo "[+] Changing MTU lo interface to 1500 ..."
#sudo ifconfig lo mtu 1500

echo "[+] Starting server with xor in bg ...";
python3 server_div_xor.py $PORT  &

#echo "[+] Starting server in bg ...";
#python3 server_div.py $PORT  &

#sleep 1s so that server starts
sleep 1

file_videolist="/home/francesco/Desktop/UniPd/thesis/master_project/videolist"
MAX_NUM_VIDEOS=56
i=0
num_video=1

while read -r line
do
  echo "--------------------- $i/$num_video ---------------------"

  if [[ $i -eq $num_video || $i -eq $MAX_NUM_VIDEOS ]];
  then
    break
  fi

  echo "[+] Starting tcpdump ..."
  out="out_div/out-"`date +"%d-%h-%Y-%H:%M:%S"`"$line.pcap"
  ./launch_tcpdump.sh $out $PORT &
  sleep 1
  #echo "[+] Client requests: $line"
  python3 client_div.py $line $PORT

  #enter in the if-body when, for example, server does not start
  # so client cannot bind to it --> error
  if [ $? -eq 1 ]
  then
    echo "[-] Error client"
    echo "[i] Removing output tcpdump: $out"
    rm $out
    #killing launch_tcpdump.sh
    kill %2
    echo "[-] Exit ..."
    exit 1
  fi

  #sleep necessary in order to have unique names
  sleep 2
  #killing 2nd bg process, i.e., launch_tcpdump
  kill %2

  #echo "[+] Creating plot and saving it ..."
  #python3 plot_packet.py $out

  #sleep necessary for avoiding problems in reading pcap file
  #sleep 1
  echo "[+] Extracting features and saving them ..."
  python3 -W ignore extract_features_div.py $out


  ((i=i+1))

done < "$file_videolist"

#kill 1st bg process, i.e., server.py
kill %1

#echo "[+] Setting MTU lo interface back to 65536"
#sudo ifconfig lo mtu 65536
