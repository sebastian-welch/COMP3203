import socket
import sys
import os

def getSize(fileName):
    st = os.stat(fileName)
    return st.st_size

def encodeLength(l):
    l = str(l)
    while len(l) < 4096:
        l = '0'+l
    return l

def decodeLength(l):
    l = str(l)
    return int(l.lstrip('0'))

s = socket.socket()
print "input server IP: "
host = sys.stdin.readline()[:-1] #'10.10.220.108'
port = 10000

s.connect((host, port))
while True:
    print "command:"
    command = sys.stdin.readline()
    command_list = command.split(' ')
    cmd = command_list[0]
    s.send(command)
    if cmd == "exit\n":
        s.close
        break
    elif cmd == "get" and len(command_list) is 2:
        f = open('server_sent-'+ (command_list[1])[:-1], 'wb')
        l = s.recv(4096)
        if "ERR: GET" not in l:
            datasize = decodeLength(l)
            s.send('y')
            l = s.recv(datasize)
            f.write(l)
            s.send('y')
        f.close()
    elif cmd == "add" and len(command_list) is 2:
        filename = (command_list[1])[:-1]
        print filename
        try:
            sendFile = open(filename)
            data = sendFile.read()
            s.sendall(encodeLength(len(data)))
            s.sendall(data)
            sendFile.close()
            s.recv(1)
            print 'completed transfer\n'
        except Exception:
            s.send("ERR: ADD")
            print "Error detected. Add command failed."
    else:
        print s.recv(4096)
