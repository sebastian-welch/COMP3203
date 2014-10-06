import socket
import sys

s = socket.socket()
host = '10.10.220.108'
port = 10000

s.connect((host, port))
while True:
    print "command:"
    command =  sys.stdin.readline()
    command_list = command.split(' ')
    cmd = command_list[0]
    s.send(command)
    if cmd == "exit\n":
        s.close
        break
    elif cmd == "get":
        print "get files"
    
    print s.recv(1024)
