import socket
import sys

s = socket.socket()
host = '192.168.0.107'
port = 10000

s.connect((host, port))
while True:
    print "command:"
    command =  sys.stdin.readline()
    print "input = ", command
    if command == "exit\n":
        s.close
        break
    s.send(command)
    print s.recv(1024)
