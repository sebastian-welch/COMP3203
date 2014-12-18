#Inq. Probe, a Python packet sniffer
#Authors: Sebastian Welch, Shawn Ellis
#Date   : December 19, 2014

import socket, sys, signal
from struct import *

#Open file for logging
log = open('InqProbeLog.txt', 'w')

#Read all packets
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error, m:
    print 'Socket could not be created.'
    

def InqProbeShutdown(sigNum, frame):
    print '\n'
    log.close()
    s.close()
    sys.exit(1)

signal.signal(signal.SIGINT, InqProbeShutdown)

#Translates the ethernet address into a dash-separated hex string 
def parseEthAddr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b

#Print ethernet packet headers
def parseEthernet(packet):
    ethLength = 14
    packedEthHeader = packet[:ethLength]
    
    #Unpacking
    ethHeader = unpack('!6s6sH', packedEthHeader)

    protocol = socket.ntohs(ethHeader[2]) #Ethernet header protocol

    print '-------ETH HEADER------'
    print 'Destination MAC: ' + parseEthAddr(packet[0:6])
    print 'Source MAC:      ' + parseEthAddr(packet[6:12])
    print 'Protocol:        ' + str(protocol)
    print '-----------------------'

    log.write('-------ETH HEADER------\n')
    log.write('Destination MAC: ' + parseEthAddr(packet[0:6]) + '\n')
    log.write('Source MAC:      ' + parseEthAddr(packet[6:12]) + '\n')
    log.write('Protocol:        ' + str(protocol))
    log.write('-----------------------\n')

#Print IP packet headers
def parseIP(packet):
    #An IP Header is 120 bits total so we need the first 20 characters of it
    IP_Header = packet[0:20]

    #Unpack the header using the unpack method from struct, first element is
    #the format, second is the binary data to unpack
    header = unpack('!BBHHHBBH4s4s', IP_Header)
   
    #Version number, bitshift is used to remove the header length from the
    #element.
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

    print '-------IP HEADER-------'
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

    log.write('-------IP HEADER-------\n')
    log.write('Version:       ' + str(version) + '\n')
    log.write('Header Length: ' + str(headerLength) + '\n')
    log.write('ToS:           ' + str(ToS) + '\n')
    log.write('Packet Length: ' + str(packLength) + '\n')
    log.write('ID Tag:        ' + str(idTag) + '\n')
    log.write('Flags:         ' + str(flags) + '\n')
    log.write('TTL:           ' + str(TTL) + '\n')
    log.write('Protocol:      ' + str(protocol) + '\n')
    log.write('Checksum:      ' + str(checksum) + '\n')
    log.write('Source IP:     ' + srcIP + '\n')
    log.write('Dest. IP:      ' + destIP + '\n')
    log.write('-----------------------\n')
    
    IPInfo = [headerLength, protocol]
    return IPInfo;

#Print TCP packet headers
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
    window = TCPHeader[6]   #Size of the receive window
    checksum = TCPHeader[7] #Error checksum

    print '-------TCP HEADER-------'
    print 'Source Port:   ' + str(srcPort)
    print 'Dest. Port:    ' + str(destPort)
    print 'Sequence #:    ' + str(SYN)
    print 'Ackn. #:       ' + str(AKN)
    print 'Data Offset:   ' + str(offset)
    print 'Header Length: ' + str(hLength)
    print 'Window Size:   ' + str(window)
    print 'Checksum:      ' + str(checksum)
    print '------------------------'

    log.write('-------TCP HEADER-------\n')
    log.write('Source Port:   ' + str(srcPort) + '\n')
    log.write('Dest. Port:    ' + str(destPort) + '\n')
    log.write('Sequence #:    ' + str(SYN) + '\n')
    log.write('Ackn. #:       ' + str(AKN) + '\n')
    log.write('Data Offset:   ' + str(offset) + '\n')
    log.write('Header Length: ' + str(hLength) + '\n')
    log.write('Window Size:   ' + str(window) + '\n')
    log.write('Checksum:      ' + str(checksum) + '\n')
    log.write('------------------------\n')

#Print UDP packet headers
def parseUDP(hLength, packet):
    packedUDPHeader = packet[hLength:hLength+8]

    #Unpacking
    UDPHeader = unpack('!HHHH', packedUDPHeader)
    
    srcPort = UDPHeader[0]  #Source port
    destPort = UDPHeader[1] #Destination port
    hLength = UDPHeader[2]  #UDP Header length
    checksum = UDPHeader[3] #Error checksum

    print '-------UDP HEADER-------'
    print 'Source Port:   ' + str(srcPort)
    print 'Dest. Port:    ' + str(destPort)
    print 'Header Length: ' + str(hLength)
    print 'Checksum:      ' + str(checksum)
    print '------------------------'

    log.write('-------UDP HEADER-------\n')
    log.write('Source Port:   ' + str(srcPort) + '\n')
    log.write('Dest. Port:    ' + str(destPort) + '\n')
    log.write('Header Length: ' + str(hLength) + '\n')
    log.write('Checksum:      ' + str(checksum) + '\n')
    log.write('------------------------\n')

while True:
    incomingPacket = s.recvfrom(65565)

    packet = incomingPacket[0]

    print '------PACKET RECEIVED------'
    log.write('------PACKET RECEIVED------\n')

    parseEthernet(packet)    #Parse ethernet header
    IPInfo = parseIP(packet) #Parse IP header

    if IPInfo[1] == 6:       #TCP Packets
        parseTCP(IPInfo[0], packet) 
    elif IPInfo[1] == 17: #UDP Packets
        parseUDP(IPInfo[0], packet)
    else:                   #Other
        print 'Non TCP or UDP header.'
        print '\n'
	log.write('Non TCP or UDP header.')
        log.write('\n')
    print '---------------------------\n'
    log.write('---------------------------\n\n') 
