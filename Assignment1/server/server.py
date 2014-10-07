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


s = socket.socket()         
IP = '192.168.0.106'
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
                    chunk = sendFile.read(1024)
                    while (chunk):
                        c.send(chunk)
                        chunk = sendFile.read(1024)
                    sendFile.close()
                    c.send("@END OF FILE@")
                    print 'completed transfer\n'
                except Exception:
                    c.send("Error: get failed")
            else:
                c.send("Invalid number of arguments for get.\n")
        elif com == 'add':
            f = open('client_sent-'+ (com_list[1]), 'wb')
            l = c.recv(1024)
            if "ERROR: add failed." not in l:
                while (l and '@END OF FILE@' not in l):
                    f.write(l)
                    l = c.recv(1024)
            f.close()
        elif com == 'exit':
            c.close()
            break
