#Inq. Probe, a Python packet sniffer
#Authors: Sebastian Welch, Shawn Ellis
#Date   : December 9, 2014

import socket
from struct import *

def parseTCP(hLength, packet):
    packedTCPHeader = packet[hLength:hLength+20]

    #Unpacking
    TCPHeader = unpack('!HHLLBBHHH', packedTCPHeader)

    srcPort = TCPHeader[0]  #Sending Port
    destPort = TCPHeader[1] #Receiving Port
    SYN = TCPHeader[2]      #Sequence Number flag
    AKN = TCPHeader[3]      #Acknowledgement Number flag
    offset = TCPHeader[4]   #Data Offset
    hLength = offset >> 4   #Length of the TCP Header
    #NS = TCPHeader[5] >> 8 & 10000000
    #CWR = TCPHeader[5] >> 7 

    print '-------TCP PACKET-------'
    print 'Source Port:   ' + str(srcPort)
    print 'Dest. Port:    ' + str(destPort)
    print 'Sequence #:    ' + str(SYN)
    print 'Ackn. #:       ' + str(AKN)
    print 'Data Offset:   ' + str(offset)
    print 'Header Length: ' + str(hLength)
    #print 'NS:            ' + str(NS)
    #print 'CWR:           ' + str(CWR)
    print '------------------------'
    print '\n'

#Set up to read raw packets
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

while True:
    incomingPacket = s.recvfrom(65565)
    packet = incomingPacket[0]

    #An IP Header is 120 bits total so we need the first 20 characters of it
    IP_Header = packet[0:20]

    #Unpack the header using the unpack method from struct, first element is
    #the format, second is the binary data to unpack
    header = unpack('!BBHHHBBH4s4s', IP_Header)
   
    #Version number, bitshift is used to remove the header length from the element
    version_length = header[0]
    version = version_length >> 4

    #Length of header is in multiples of 4 bytes so multiply length by 4
    #Bit operation is used to set the version bits to 0
    headerLength = (version & 0xF) * 4
    ToS = header[1]         #Type of service, priority of the packet
    packLength = header[2]  #Length of the packet
    idTag = header[3]       #identification tag of the packet
    flags = header[4] >> 13 #Flags, bitshifted to remove the fragment offset
    TTL = header[5]         #Time to live
    protocol = header[6]    #TCP, UDP, etc.
    checksum = header[7]    #Used for error detection

    #inet_ntoa converts a 32-bit packed IPv4 address into string format
    srcIP = socket.inet_ntoa(header[8])       #Source IP
    destIP = socket.inet_ntoa(header[9])      #Destination IP

    print '-------IP PACKET-------'
    print 'Version:       ' + str(version)
    print 'Header Length: ' + str(headerLength)
    print 'ToS:           ' + str(ToS)
    print 'Packet Length: ' + str(packLength)
    print 'ID Tag:        ' + str(idTag)
    print 'Flags:         ' + str(flags)
    print 'TTL:           ' + str(TTL)
    print 'Protocol:      ' + str(protocol)
    print 'Checksum:      ' + str(checksum)
    print 'Source IP:     ' + srcIP
    print 'Dest. IP:      ' + destIP
    print '-----------------------'
    print '\n'

    #TCP Packets
    if protocol == 6:
       parseTCP(headerLength, packet)
