import numpy as np
import socket
import sys

PORT=int(sys.argv[1])
MTU=65536-20-20 #remove IP and TCP headers

#get ip address of my machine
def get_ipAddr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def parse_request(raw_req):
    try:
        req = str(raw_req).split(" ")
        method=str(req[0])
        resource=str(req[1])
        return method, resource
    except Exception as e:
        print("[-] Error:"+e)
    return None

if __name__ == "__main__":
    #redirect output to file
    #sys.stdout = open('log_server.txt', 'a')

    ip_server = get_ipAddr()
    #TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip_server,PORT))
    #at most 5 unaccepted connections
    # before the system refuses new connections
    server.listen(5)
    print("[+] Server listening on "+str(ip_server)+":"+str(PORT))

    while(1):
        try:
            #print("*"*80)
            (client,client_addr) = server.accept()
            ip_client = client_addr[0]
            port_client = client_addr[1]
            print("[+] Client "+str(ip_client)+":"+str(port_client)+" connected to server")
            data = str(client.recv(MTU))
            #print("[i] Raw data received: "+str(data))
            method,resource_raw = parse_request(data)
            #print("[i] requested resource :"+resource_raw)
            resource = resource_raw.split("/")[-1]
            #print("resource:"+resource)
            file_name="/home/francesco/Desktop/UniPd/thesis/master_project/videos/"+resource
            f = open(file_name,"rb")
            data_read = f.read(MTU)
            print("[i] Sending data ...")
            while(data_read):
                #print("[i] Sending video sample ...")
                client.send(data_read)
                for i in range(100):
                    mtu_fake = np.random.binomial(n=MTU*2, p=0.5)
                    if mtu_fake < MTU:
                        break
                data_read = f.read(mtu_fake)
            f.close()
            #print("[i] Closing conn with "+str(client))
            client.close()

        except KeyboardInterrupt:
            #close fd socket before exiting
            print("[+] Closing socket ...")
            server.close()
            print("[i] Keyboard Interrupt\nExit ...")
            sys.exit(0)

        except Exception as e:
            print("[-] Error:"+str(e))
