from socket import socket
import threading

class ClientText:
    PORT = 50052
    clientSocket = None

    @staticmethod
    def start():
        clientSocket = socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(('', PORT))

    @staticmethod
    def sendMsg(msg):
        while True:
            clientSocket.send(msg)