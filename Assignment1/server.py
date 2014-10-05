import socket

s = socket.socket()
host = socket.gethostname()
port = 10000
s.bind((host, port))

s.listen(5)
while True:
    c, addr = s.accept()
    print 'Connected to: ', addr
    c.send('Get good nerd')
    c.close()
