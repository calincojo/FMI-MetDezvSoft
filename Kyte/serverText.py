import socket
import threading
from Queue import Queue

rcvTextQueue = Queue(10)

def startTextServer(socketServer) :
    CHUNK = 1024
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 50052  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f = s.makefile()
    s.bind((HOST, PORT))
    s.listen(1)

    print 'Server Text Started'

    socketServer, addr = s.accept()

    #conn.close()

def sendData(s, CHUNK):
    while True:
        data = raw_input()
        s.sendall(data)

def receiveData(s, CHUNK):
    print '[receiveData]'
    data = s.recv(1024)
    while 1:
        data = s.recv(1024)
        print '[receiveData] Received ' + data
        rcvTextQueue.put(data)
