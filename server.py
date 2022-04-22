import socket, cv2
import imutils, sys
import numpy as np
import base64, time, os
from  cryptography.fernet import Fernet
from udpstructure import UDPPacket

group = '224.1.1.1'
port= 9999

ttl =2
sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

sockaddress=(group, port)
sock.settimeout(0.2)

print("broadcasting from", sockaddress)
vid =cv2.VideoCapture(0)
fps,st,frames_to_count,cnt = (0,0,20,0)
data=0
key=Fernet.generate_key()
msg=b'Hello'
fernet = Fernet(key)

sock.sendto(b'Hello world', sockaddress)



while data < 1000:
    print('GOT connection from ',sockaddress)
    WIDTH=400
    while(vid.isOpened()):
        _,frame = vid.read()
        mydata="{}".format(frame)
        udp=UDPPacket(mydata)
        udp.assemble_udp_feilds()
        rawData=udp.raw
        print("UDP packetts")
        print(UDPPacket(mydata))
        frame = imutils.resize(frame,width=WIDTH)
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buffer)
        sock.sendto(message,sockaddress)
        #sock.sendto(encMsg,sockaddress)
        frame = cv2.putText(frame,'FPS: ',(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        #cv2.imshow('TRANSMITTING VIDEO',frame)
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
