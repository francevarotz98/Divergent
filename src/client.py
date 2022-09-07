import socket
#import os
import sys

HOST = "192.168.1.12"  # The server's hostname or IP address
PORT = int(sys.argv[2])  # The port used by the server
MTU = 65536-20-20 #remove IP and TCP header


#get ip address of my machine
def get_ipAddr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

if __name__ == "__main__":

    HOST = get_ipAddr()
    #videos=os.listdir("/home/francesco/Desktop/UniPd/thesis/master_project/videos")
    video = sys.argv[1]
    #print("[i] requesting video:"+video)

    req = b"GET /videos/"+video.encode()+b" HTTP/1.1\r\n\r\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(req)
        data = s.recv(MTU)
        while(data):
            data = s.recv(MTU)

    print("[i] client received all data ... ")
