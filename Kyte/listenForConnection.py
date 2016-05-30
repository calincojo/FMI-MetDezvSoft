__author__ = 'Cojocaru'

import socket
import main

def listenForConnection() :
  #  main.chatWindow(1)
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50030              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    #   main.chatWindow(addr)
    print "Hei"
    conn.close()
    s.close()

def tryConnect(IP) :
    HOST = IP    # The remote host
    PORT = 50030              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('Hello, world')
    s.close()




