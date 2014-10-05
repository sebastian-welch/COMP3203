import socket               
import subprocess

s = socket.socket()         
IP = '192.168.0.107'
port = 10000
s.bind((IP, port))       

s.listen(5)
c, addr = s.accept()
while True:
  com = c.recv(5)

  print com;

  if com == 'ls\n':
    contents = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE)
    out, err = contents.communicate()
    c.send(out)
