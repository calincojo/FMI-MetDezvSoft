__author__ = 'Cojocaru'

from Tkinter import *
import textWindow
import clientAudio
import clientVideo
import serverVideo
import  serverAudio
import serverText
import clientText
import threading
import listenForConnection
import time
import socket
from Queue import Queue


root = ''
queue = ''
MYNAME = "Calin"
threadAudioServer = ''
threadVideoServer = ''
threadTextServer = ''

socketClientText = ''
socketServerText = ''
'''

th = threading.Thread(group=None, target=serverVideo.startVideoServer, args=(), kwargs={})
th.start()
th = threading.Thread(group=None, target=clientAudio.audioServer, args=(), kwargs={})
th.start()
time.sleep(5)
th = threading.Thread(group=None, target=clientAudio.audioClient, args=(), kwargs={})
th.start()
clientVideo.videoClient()

'''


def listenForConnection() :
  #  main.chatWindow(1)
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50030              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    queue.put(1)
    #   main.chatWindow(addr)

    conn.close()
    s.close()

def tryConnect(IP) :
    HOST = IP    # The remote host
    PORT = 50030              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('Hello, world')
    s.close()

#start the servers for all type of communication at program startup
def startServers():
    '''
    threadVideoServer = threading.Thread(group=None, target=serverVideo.startVideoServer, args=(), kwargs={})
    threadVideoServer.start()
    threadAudioServer = threading.Thread(group=None, target=clientAudio.audioServer, args=(), kwargs={})
    threadAudioServer.start()
    '''

    threadTextServer = threading.Thread(group=None, target=serverText.startTextServer, args=(socketServerText,), kwargs={})
    threadTextServer.start()

    th = threading.Thread(group=None, target=listenForConnection, args=(), kwargs={})
    th.start()


def Call():
    #todo start the audio and video client in order to connect with the server
    return

def sendTextMessage(message, destTxt, s):

    content = message.get("1.0",END)
    destTxt.config(state=NORMAL)
    destTxt.insert(END, MYNAME + " :"+ content)
    destTxt.config(state=DISABLED)
    s.sendall(content)

def getTextMessage(destTxt, s):
    while True:
        data = s.recv(1024)
        destTxt.config(state=NORMAL)
        destTxt.insert(END, "Name" + " :"+ data)
        destTxt.config(state=DISABLED)

def chatWindow(IPtoConnect):

    window = Tk()

    leftFrame = Frame(window,bg="black",  cursor="dot")
    rightFrame = Frame(window,width=1000)

    serverVideoFrame = Frame(rightFrame, bg="red")
    clientVideoFrame = Frame(rightFrame)

    callButton = Button(rightFrame, text="Call", command = lambda : Call())

    serverVideoFrame.pack(side=TOP)
    callButton.pack(side = BOTTOM, fill = X)
    clientVideoFrame.pack(side=BOTTOM)

    l = Label(serverVideoFrame, text="server Video",width=50)
    l.pack(side = TOP)

    l = Label(clientVideoFrame, text="client Video")
    l.pack(side = BOTTOM)

    leftFrame.pack(side=LEFT)
    rightFrame.pack(side=LEFT, fill = BOTH)

    messagesWindow = textWindow.textWindow(leftFrame,400,400)
    messagesWindow.txt.config(state=DISABLED)

    textMessageWindow = textWindow.textWindow(leftFrame,200,100)

    #sendMsgBtn = Button(leftFrame, text="Send message", command= lambda : sendTextMessage(textMessageWindow.txt, messagesWindow.txt))
    #sendMsgBtn.pack(fill=BOTH)

    #th= threading.Thread(group=None, target=sendData, args=(), kwargs={})
    #th.start()

    window.mainloop()

def startChatSession( IPtoConnect):
    print IPtoConnect
    tryConnect(IPtoConnect)
    chatWindow(IPtoConnect)
    return


def checkIncomingConnection():
    if queue.empty():
        root.after(2000, checkIncomingConnection)
    else:
        print "DA"
        chatWindow(1)

def Main():

    startServers()
    root.resizable(False,False)

    nameToIP = {"renata" : "192.168.2.230", "calin" : "192.168.2.31" }

    l = Label(root, text="---Online users---",bg="blue")
    l.pack(fill=X)

    b = Button(root, text="Calin", command= lambda: startChatSession(nameToIP["calin"]), width = 45)
    b.pack(fill=BOTH)
    b = Button(root, text="Renata", command= lambda: startChatSession(nameToIP["renata"]) )
    b.pack(fill=BOTH)

    root.after(2000,checkIncomingConnection)
    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    queue =Queue()
    Main()

