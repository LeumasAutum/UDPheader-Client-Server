
import socket, struct, cv2, base64
import numpy as np
import time
import sys, zlib

from udpstructure import *

from  cryptography.fernet import Fernet


MCAST_GRP='224.1.1.1'
MCAST_PORT=9999
BUFF_SIZE = 65536
sockaddresss=(MCAST_GRP,MCAST_PORT)

for i in range (0,10):
    connid = i+1

sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,BUFF_SIZE)

sock.bind(('', MCAST_PORT))

mreq=struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

msg=b'hello'

key=Fernet.generate_key()
msg=b'Hello'
fernet = Fernet(key)

print(f"connection started {connid}")

fps,st,frames_to_count,cnt = (0,0,20,0)

while True:
    #print(sock.recv(10240))
    packet,_ = sock.recvfrom(BUFF_SIZE)
    checksum=zlib.crc32(packet)
    

    print(f"udp header contains/n  Length :{len(packet)} bytes /n from {MCAST_GRP}/n on port {MCAST_PORT} from port {UDPPacket.assemble_udp_feilds}the checksum is {checksum}")
    
    data = base64.b64decode(packet,' /')
    
    npdata = np.frombuffer(data,dtype=np.uint8)
    frame = cv2.imdecode(npdata,1)
    
    #UDPPacket.assemble_udp_feilds(self, self.raw)
    frame = cv2.putText(frame,'',(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        sock.close()
        break
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count/(time.time()-st))
            st=time.time()
            cnt=0
        except:
            pass
    cnt+=1
    decMsg=fernet
