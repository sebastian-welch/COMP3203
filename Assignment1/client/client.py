import socket
import sys
import os

def getSize(fileName):
    st = os.stat(fileName)
    return st.st_size

def encodeLength(l):
    l = str(l)
    while len(l) < 1500:
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
        #Adding file to the client side
        f = open('server_sent-'+ (command_list[1])[:-1], 'wb')
        size = int(s.recv(1024))
        s.send(b'0')
        recving = 0
        while size > recving:
            data = s.recv(4013)
            recving += len(data)
            f.write(data)
        f.flush()
        f.close()
    elif cmd == "add" and len(command_list) is 2:
        #Adding files to the server
        fileName = (command_list[1])[:-1]
        f = open(fileName, 'rb')
        size = s.sendall(bytes(os.path.getsize(fileName)))
        s.recv(32)
        sending = 0
        while os.path.getsize(fileName) > sending:
          sending += s.send(f.read(4013))
        f.close()
    else:
        print s.recv(4096)
