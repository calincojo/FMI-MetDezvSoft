import socket
import threading

def startTextClient(socketClient) :
    HOST = 'localhost'#'192.168.2.31'   # The remote host
    TEXT_PORT = 50052  # The same port as used by the server

    CHUNK = 1024
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.connect((HOST, TEXT_PORT))

    print 'Starting data transmission...'
   # tup = (s, CHUNK)
    #th= threading.Thread(group=None, target=sendData, args=(tup), kwargs={})
    #th.start()
    #th = threading.Thread(group=None, target=receiveData, args=(tup), kwargs={})
    #th.start()

    #print 'done transmission'

    #s.close()

    #print 'closed'


def sendData(s, CHUNK):
    while True:
        data = raw_input()
        s.sendall(data)

def receiveData(s, CHUNK):
    data = s.recv(1024)
    while data !='':
        print data
        data = s.recv(1024)

startTextClient()