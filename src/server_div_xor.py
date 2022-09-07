import socket
import sys
import secrets #module for generating random numbers. it exploits
import os
import numpy as np

#https://blog.cloudflare.com/ensuring-randomness-with-linuxs-random-number-generator/

'''
    SECRET_NUMBER generato in modo t.c. per le risorse più grandi
    io abbia un SECRET_NUMBER più grande, probabilisticamente parlando, (
    in quanto + grande SECRET_NUMBER, meno dummy pkt saranno trasmessi)
    viceversa per risorse più piccole. in questo modo traffic flow di risorse
    più piccole saranno più simili a traffic flow di quelle più grandi.
'''
try:
    PORT = int(sys.argv[1])
except IndexError:
    PORT = 4447

MTU  = 65536-20-20 #remove IP and TCP headers
THRESHOLD_FILE_SIZE = 10600000 #threshold for size of files requested, which
                               #  define which binomial distribution to use for
                               #  generating SECRET_NUMBER
SECRET_NUMBER = 0

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

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

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

    #pay_pkt counts the payload of real packets
    pay_pkt = 0

    while(1):
        try:
            (client,client_addr) = server.accept()
            ip_client   = client_addr[0]
            port_client = client_addr[1]
            print("[+] Client "+str(ip_client)+":"+str(port_client)+" connected to server")
            data = str(client.recv(MTU))
            method,resource_raw = parse_request(data)
            print("[i] requested resource :"+resource_raw)
            resource  = resource_raw.split("/")[-1]
            file_name = "/home/francesco/Desktop/UniPd/thesis/master_project/videos/"+resource
            #length of file_name in [byte]
            byte_size = os.stat(file_name).st_size

            while SECRET_NUMBER == 0:
                #draw SECRET_NUMBER from binomial distribution which depends
                # on the size of the file
                if byte_size > THRESHOLD_FILE_SIZE:
                    SECRET_NUMBER = np.random.binomial(n=10, p=0.5) #secrets.randbelow(6) #at most 5
                else:
                    SECRET_NUMBER = np.random.binomial(n=6, p=0.5)

            #print("[D] sending random number",SECRET_NUMBER)
            #before sending the requested data, send the random number
            client.send(b"Random_dummy:"+str(SECRET_NUMBER).encode())

            f = open(file_name,"rb")

            data_read = f.read(MTU)
            pay_pkt +=1

            print("[i] Sending data ...")
            #index_random_dum used to count when sending dummy pkt
            index_random_dum = 0
            while(data_read):
                if index_random_dum < SECRET_NUMBER:
                    index_random_dum += 1
                    client.send(data_read)
                    #compute a "fake" mtu, which is sampled
                    # from Bin(MTU*2, 0.5)
                    for i in range(100):
                        mtu_fake = np.random.binomial(n=MTU*2, p=0.5)
                        if mtu_fake < MTU:
                            break

                    data_read = f.read(mtu_fake)
                    pay_pkt +=1
                    prev_pkt = pay_pkt

                #if index is equal to SECRET_NUMBER, then send dummy packet
                # and reset index back to 0
                else:
                    #num_burst represents how many consecutive
                    # dummy packets we send
                    num_burst = np.random.binomial(n=8, p=0.5)
                    #variable needed for choosing if inserting payload to
                    # next burst of dummy packets or not.
                    # 0 -> has not payload
                    # 1 -> has payload
                    has_payload = secrets.randbelow(2)
                    for i in range (num_burst):
                        #length of dummy packet is taken from Bin(MTU,0.5)
                        for i in range(100):
                            len_dummy = np.random.binomial(n=MTU*2, p=0.5)
                            if len_dummy < MTU:
                                break
                        #send dummy with pyaload which is the xor of the
                        # next packet to be sent, with the following one
                        if has_payload:
                            next_data_read = b"dummy_payload"
                            next_data_read += f.read(len_dummy) if len_dummy < MTU else f.read(MTU)

                            pay_pkt +=1
                            #print(f"[D] xoring pkt {pay_pkt} with {prev_pkt}")

                            xor_payload = byte_xor(next_data_read,data_read)
                            dummy_pkt = b"dummy_payload"+xor_payload
                            client.send(dummy_pkt)
                            data_read = next_data_read
                        #send dummy without payload
                        else:
                            dummy_pkt = b"dummy"+secrets.token_bytes(len_dummy)
                            #print("[D] len(dummy_pkt):",len(dummy_pkt))
                            client.send(dummy_pkt)
                    index_random_dum = 0

            #reset index and SECRET_NUMBER (will be reset next in while-loop)
            index_random_dum = 0
            SECRET_NUMBER    = 0
            f.close()
            print("[i] Closing conn with "+str(ip_client)+":"+str(port_client))
            client.close()
            #print("-"*80)

        except KeyboardInterrupt:
            #close fd socket before exiting
            print("[+] Closing socket ...")
            server.close()
            print("[i] Keyboard Interrupt\nExit ...")
            sys.exit(0)

        except Exception as e:
            print("[-] Error:"+str(e))
