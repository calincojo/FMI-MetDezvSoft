__author__ = 'Cojocaru'

from Tkinter import *
import textWindow
import clientAudio
import clientVideo
import serverVideo
import  serverAudio
import threading
import time
'''
th = threading.Thread(group=None, target=serverVideo.startVideoServer, args=(), kwargs={})
th.start()
th = threading.Thread(group=None, target=clientAudio.audioServer, args=(), kwargs={})
th.start()
time.sleep(5)
th = threading.Thread(group=None, target=clientAudio.audioClient(), args=(), kwargs={})
th.start()
clientVideo.videoClient()
'''


def callback():
    print "click!"

def Call():
    return

def sendTextMessage(message, destTxt):
    content = message.get("1.0",END)
    print content
    destTxt.config(state=NORMAL)
    destTxt.insert(END,content)
    destTxt.config(state=DISABLED)


def newWindow():
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

    sendMsgBtn = Button(leftFrame, text="Send message", command= lambda : sendTextMessage(textMessageWindow.txt, messagesWindow.txt))
    sendMsgBtn.pack(fill=BOTH)



    window.mainloop()


root = Tk()

root.resizable(False,False)

l = Label(root, text="---Online users---",bg="blue")
l.pack(fill=X)

b = Button(root, text="Calin", command=newWindow, width = 45)
b.pack(fill=BOTH)
b = Button(root, text="Renata", command=callback)
b.pack(fill=BOTH)


root = mainloop()
