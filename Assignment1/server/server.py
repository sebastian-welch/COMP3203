import socket               
import subprocess
import sys
import signal
import os

#interrupt handler to clean up when quitting during listening section
def signal_handler_listening(signal, frame):
    s.close()
    sys.exit(0)

#interrupt handler to clean up when quitting during receiving/sending section
def signal_handler_receiving(signal, frame):
    c.close()
    s.close()
    sys.exit(0)

#get size of file
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
print "input IP: "
IP = sys.stdin.readline()[:-1] #'10.10.220.108'
port = 10000
s.bind((IP, port))       

while True:
    signal.signal(signal.SIGINT, signal_handler_listening)
    #Waits for a connection and then accepts it
    s.listen(10)
    c, addr = s.accept()
    while True:
        signal.signal(signal.SIGINT, signal_handler_receiving)
        #Waits for command from the client
        communication = c.recv(200)
        #Removes the \n 
        communication = communication[:-1]
        #Parses the string into a list, separated by ' '
        com_list = communication.split(' ')
        com = com_list[0];
        print "Received command: ", communication
        if com == 'ls': #LS command
            #Pipes the contents of the ls into a variable
            contents = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE)
            out, err = contents.communicate()
            c.send(out)
        elif com == 'get': #Getting files from the server
            if len(com_list) is 2:
                fileName = com_list[1]
                print fileName
                try:
                    sendFile = open(fileName)   
                    data = sendFile.read()
                    c.sendall(encodeLength(len(data)))
                    c.recv(1)
                    c.sendall(data)
                    sendFile.close()
                    c.recv(1)
                    print 'completed transfer\n'
                except Exception:
                    c.send("ERR: GET")
            else:
                c.send("Invalid number of arguments for get.\n")
        elif com == 'add':
            f = open('client_sent-'+ (com_list[1]), 'wb')
            l = c.recv(4096)
            if "ERR: ADD" not in l:
                datasize = decodeLength(l)
                l = c.recv(datasize)
                f.write(l)
                c.send('0')
            f.close()
        elif com == 'exit':
            c.close()
            break
