import struct, socket

class UDPPacket():

  def __init__(self, data=0, dport = 80, sport = 65535, dst='127.0.0.1', src='192.168.1.101'):
    
    self.dport = dport
    self.sport = sport
    self.src_ip = src
    self.dst_ip = dst
    self.data   = data
    self.raw = None
    self.create_udp_feilds()
    print(self.data)

  def assemble_udp_feilds(self):
    self.raw = ['!HHLLBBHHH', # Data Structure Representation
    self.udp_src,   # Source IP
    self.udp_dst,    # Destination IP
    self.udp_seq,    # Sequence
    self.udp_ack_seq,  # Acknownlegment Sequence
    self.udp_hdr_len,   # Header Length
    self.udp_flags ,    # udp Flags
    self.udp_wdw,   # udp Windows
    self.udp_chksum,  # udp cheksum
    self.udp_urg_ptr # udp Urgent Pointer
    ]
    print("Source IP: {} ".format(self.udp_src))
    print("destination port: {}".format(self.udp_dst))
    print("flags are: {}".format(self.udp_seq))
    print("Ack Sequence: {}".format(self.udp_ack_seq))
    print("Header length: {}".format(self.udp_hdr_len))
    print("UDP Window: {}".format(self.udp_wdw))
    print("UDP Checksum: {}".format(self.udp_chksum))
    print("UDP urgent Pointer: {}".format(self.udp_urg_ptr))
    

    self.calculate_chksum() # Call Calculate CheckSum
    return


  def reassemble_udp_feilds(self):
    self.raw = struct.pack('!HHLLBBH', 
     self.udp_src, 
     self.udp_dst, 
     self.udp_seq, 
     self.udp_ack_seq, 
     self.udp_hdr_len, 
     self.udp_flags , 
     self.udp_wdw) + struct.pack("H", 
     self.udp_chksum) + struct.pack('!H', 
     self.udp_urg_ptr)
    print((self.raw).hex())
    print(self.raw) #PUTBACK
    return

  def calculate_chksum(self):
    src_addr     = socket.inet_aton( self.src_ip )
    dest_addr    = socket.inet_aton( self.dst_ip )
    placeholder  = 0
    protocol     = socket.IPPROTO_UDP
    udp_len      = len(self.raw) + len(self.data)

    if protocol == 17:
      print("protocol: UDP")
   
    psh = struct.pack('!4s4sBBH' , 
     src_addr , 
     dest_addr , 
     placeholder , 
     protocol , 
     udp_len
     )

    #psh = psh + base64.b64decode(self.raw)  + self.data
    psh = ("{0}{1}{2}".format(psh, self.raw, self.data))

    self.udp_chksum = self.chksum(psh)
    
    self.reassemble_udp_feilds()
    
    return 


  def chksum(self, msg):
    s = 0  # Binary Sum

    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):

     a = ord(msg[i]) 
     b = ord(msg[i])
     s = s + (a+(b << 8))
     
    
    # One's Complement
    s = s + (s >> 16)
    s = ~s & 0xffff
    return s

  def create_udp_feilds(self):
    # ---- [ Source Port ]
    self.udp_src = self.sport

    # ---- [ Destination Port ]
    self.udp_dst = self.dport

    # ---- [ UDP Sequence Number]
    self.udp_seq = 0

    # ---- [ UDP Acknowledgement Number]
    self.udp_ack_seq = 0

    # ---- [ Header Length ]
    self.udp_hdr_len = 80

    # ---- [ UDP Flags ]
    udp_flags_rsv = (0 << 9)
    udp_flags_NACK = (0 << 8)
    udp_flags_CON = (0 << 7)
    udp_flags_DIS = (0 << 6)
    udp_flags_BUFF = (0 << 5)
    udp_flags_ack = (0 << 4)
    udp_flags_psh = (0 << 3)
    udp_flags_rst = (0 << 2)
    udp_flags_FUT = (1 << 1)
    udp_flags_FUT = (0)


    self.udp_flags = udp_flags_rsv + udp_flags_NACK + udp_flags_CON + \
          udp_flags_DIS + udp_flags_BUFF + udp_flags_ack + \
          udp_flags_psh + udp_flags_rst + udp_flags_FUT + udp_flags_FUT
    print('flags here')
    print(self.udp_flags)
    # ---- [ UDP Window Size ]
    self.udp_wdw = socket.htons (5840)

    # ---- [ UDP CheckSum ]
    self.udp_chksum = 0

    # ---- [ UDP Urgent Pointer ]
    self.udp_urg_ptr = 0


    return 
    
