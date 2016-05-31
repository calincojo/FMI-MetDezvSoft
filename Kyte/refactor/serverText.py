import socket
import threading
from Queue import Queue

class ServerText:
    PORT = 50053
    
    @staticmethod
    def startTextServer(socketServer):
        CHUNK = 1024
        HOST = ''  # Symbolic name meaning all available interfaces
        PORT = 50053  # Arbitrary non-privileged port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        f = s.makefile()
        s.bind((HOST, PORT))
        s.listen(1)

        print 'Server Text Started'

        socketServer, addr = s.accept()
        receiveData(s, 1024)

        #conn.close()
    @staticmethod
    def sendData(s, CHUNK):
        while True:
            data = raw_input()
            s.sendall(data)
    @staticmethod
    def receiveData(s, CHUNK):
        print '[receiveData]'
        data = s.recv(CHUNK)
        while 1:
            data = s.recv(CHUNK)
            print '[receiveData] Received ' + data
            rcvTextQueue.put(data)
