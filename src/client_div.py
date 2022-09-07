import socket
#import os
import sys

HOST = "192.168.1.12"  # The server's hostname or IP address
PORT = int(sys.argv[2])  # The port used by the server
MTU = 65536-20-20 #remove IP and TCP headers
SECRET_NUMBER = -1
HEADER_DUMMY = "dummy"
HEADER_DUMMY_PAYLOAD = "dummy_payload"

#get ip address of my machine
def get_ipAddr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

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
        try:
            SECRET_NUMBER = int(str(data).split(":")[1][:-1]) #that [:-1] for removing apix (')
        except:
            SECRET_NUMBER = int(str(data).split(":")[1].split("\\")[0]) #int(str(data).split(":")[1].split("\\")[0][:-1])

        #first_cycle = 1

        while(data):
            #if not first_cycle:
            #    prev_data = data
            data = s.recv(MTU)
            if str(data[0:15])[2:15] == HEADER_DUMMY_PAYLOAD:
                #TODO: implement recover payload using xor
                '''
                is_dummy_pay = 1
                while(is_dummy_pay):
                    #print("[D] dummy w/ payload")
                    #print(str(data[0:15])[2:15])
                    #print("[D] data:",data[:30])
                    #print("[D] xor:",byte_xor(data,prev_data))
                    data = s.recv(MTU)
                    if not (str(data[0:15])[2:15] == HEADER_DUMMY_PAYLOAD):
                        is_dummy_pay = 0
                '''
                pass
            elif str(data[0:5])[2:7] == HEADER_DUMMY:
                pass
                #print("[D] dummy w/out payload")
            elif len(data[0:5]) == 0 :
                #succede che ogni tanto riceva dummy vuoto: bypassare
                pass

            #first_cycle = 0
            #print("-"*80)


    print("[i] client received all data ... ")
