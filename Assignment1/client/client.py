import socket
import sys
import os

def getSize(fileName):
    st = os.stat(fileName)
    return st.st_size

s = socket.socket()
host = '192.168.0.106'
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
            l = s.recv(1024)
            if "Error: get failed" not in l:
                while (l and '@END OF FILE@' not in l):
                    f.write(l)
                    l = s.recv(1024)
            f.close()
    elif cmd == "add" and len(command_list) is 2:
        filename = command_list[1]
        print filename
        try:
            sendFile = open(filename)
            chunk = sendFile.read(1024)
            while (chunk):
                s.send(chunk)
                chunk = sendFile.read(1024)
            sendFile.close()
            s.send("@END OF FILE@")
            print 'completed transfer\n'
        except Exception:
            s.send("ERROR: add failed.")
            print "Error detected. Add command failed."
    else:
        print s.recv(1024)
