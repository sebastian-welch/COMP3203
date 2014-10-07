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

s = socket.socket()
print "input IP: "
IP = sys.stdin.readline()[:-1]
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
        elif com == 'get': #Sending files to the client
            try:
              fileName = com_list[1]
              f = open(fileName, 'rb')
              size = c.sendall(bytes(os.path.getsize(fileName)))
              c.recv(32)
              sending = 0
              
              while os.path.getsize(fileName) > sending: 
                sending += c.send(f.read(4013))
              f.close()
            except Exception:
              c.send("ERR: FILE UNREACHABLE, DISCONNECTING\n")
              c.close()
              break;
        elif com == 'add': #Receiving files from the client
            try:
              f = open('client_sent-'+ com_list[1], 'wb')
              size = int(c.recv(1024))
              c.send(b'0')
              recving = 0
              while size > recving:
                data = c.recv(4013)
                recving += len(data)
                f.write(data)
              f.flush()
              f.close()
            except Exception:
                c.send("ERR: ADD FAILED, DISCONNECTION\n")
                c.close()
                break
        elif com == 'exit':
            c.close()
            break
        else:
            print "Command not recognized\n"
