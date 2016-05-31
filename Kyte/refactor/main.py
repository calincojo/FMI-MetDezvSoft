import sys
import logging
from socket import socket
from Queue import Queue
from threading import Thread
from time import sleep

# GUI modules
from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import textWindow

# Custom modules
from chatLogger import logger

from clientText import ClientText
from serverText import ServerText

import clientAudio
import serverAudio

import clientVideo
import serverVideo

#localhost = '192.168.0.2'
localhost = '10.11.117.117'

# Define the queues for synchronization
sendMsgQueue = Queue(10)
rcvMsgQueue = Queue(10)

incomingPeer = None
INCOMING_PORT = 1235

class ContactList:
	contactBtns = {}
	chat = None
	@staticmethod
	def addnew():
		logger.info('Add new contact to the list')
		new_user = tkSimpleDialog.askstring("User", "Enter user you want to add to the Contact List")
		logger.info('new_user ' + new_user + ' Chat.myname ' + Chat.myname + ' ' + new_user.strip() == Chat.myname.strip())
		if new_user == Chat.myname:
			logger.error('You can\'t chat with yourself.')
			tkMessageBox.showerror('No life', 'Viata de programator')
		elif NamingService.lookup(new_user) != 'null':
			logger.info('The user ' + new_user + ' is valid.')
			b = Button(top, text = new_user, command = lambda: Comunication.startSession(new_user, NamingService.lookup(new_user)), width = 45)
			b.pack(fill = BOTH)
			ContactList.contactBtns[new_user] = b;
		else:
			logger.error('The user ' + new_user + ' doesn\'t exist.')
			tkMessageBox.showerror('Invalid user', 'The contact you tried to add is invalid')
	@staticmethod
	def remove():
		logger.info('Remove a contact from the list')
		user = tkSimpleDialog.askstring("User", "Enter user you want to remove from the Contact List")
		if ContactList.contactBtns.has_key(user):
			logger.info('Remove the contact')
			ContactList.contactBtns[user].pack_forget()
			del ContactList.contactBtns[user]
		else:
			logger.info('The user ' + user + ' is invalid.')
			tkMessageBox.showerror('Invalid user', 'The contact you tried to remove is invalid')

class NamingService:
	HOST = localhost
	PORT = 1234

	@staticmethod
	def add(new_user):
		logger.info('Add a new user to the Naming Service: ' + new_user)
		s = socket();
		s.connect((NamingService.HOST, NamingService.PORT))
		s.send('add ' + new_user)
		s.close()
	@staticmethod
	def lookup(user):
		logger.info('Lookup the IP address in the Naming Service for the user: ' + user)
		s = socket()
		s.connect((NamingService.HOST, NamingService.PORT))
		s.send('lookup ' + user)
		msg = s.recv(1024)
		s.close()
		logger.info('IP: ' + msg)
		return msg

class Comunication:
	peerName = None
	peerSocket = None

	@staticmethod
	def startSession(peerName, peerIP):
		# Setup some Comunication data about the peer
		Comunication.peerName = peerName

		'''
		s = socket()
		print (peerIP, INCOMING_PORT)
		s.connect((peerIP, INCOMING_PORT))
		s.send(peerName)
		s.close()
		try:
			s = socket()
			s.connect((peerIP, ServerText.PORT))
			Comunication.peerSocket = s
		except Exception, exc:
			print "Caught exception socket.error : %s" % exc
		'''
		window = Toplevel(root)
		window.title('Conversation with ' + peerName)

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

		sendMsgBtn = Button(leftFrame, text="Send message", command= lambda : Comunication.sendMsg(textMessageWindow.txt, messagesWindow.txt))
		sendMsgBtn.pack(fill=BOTH)
	@staticmethod
	def sendMsg(message, destTxt):
		# TODO clear the value from the textWindow
		content = message.get("1.0", END)
		sendMsgQueue.put(content)
		logger.info('Schedule to send message ' + content + ' to ' + Comunication.peerName)

class Chat:
	myname = None

# Setup the GUI with Tkinter
root = Tk()
root.geometry("450x250+500+300")
root.resizable(False, False)

# Ask for the user id
Chat.myname = tkSimpleDialog.askstring("User", "What is your name? (user id)");
NamingService.add(Chat.myname)

# Accept invitation to join a conversation
def listenForInvitation():
	logger.info('Started thread that waits an invitation to conversation from peers')
	s = socket()
	s.bind(('', INCOMING_PORT))
	s.listen(1)
	(c, addr) = s.accept()
	incomingPeer = c.recv(1024)
th = Thread(target = listenForInvitation)
th.start()

CHECK_INVITATION_INTERVAL = 4000
def checkInvitation():
    if incomingPeer == None:
    	logger.debug('There is no incoming peer inviting you to a conversation')
        root.after(CHECK_INVITATION_INTERVAL, checkInvitation)
    else:
        logger.info('You have been invited to a conversation by ' + incomingConnection)
        Comunication.startSession(incomingPeer, NamingService.lookup(incomingPeer))
root.after(CHECK_INVITATION_INTERVAL, checkInvitation)

root.title('Kyte - Videoconferencing - ' + Chat.myname)
# Setup the GUI layout
top = Frame(root)
top.pack(side = TOP)

bottom = Frame(root)
bottom.pack(side = BOTTOM)

b = Button(bottom, text = 'Add Contact', command = ContactList.addnew)
b.pack()
b = Button(bottom, text = 'Delete Contact', command = ContactList.remove)
b.pack()

## Peer-to-peer network - Each peer can act both as a client and as a server during comunication
# Check for incoming chat invitations thread


### Sychronization
SLEEP_AMNT = 8

# Check for sent text messages thread
def checkSendMsg():
	logger.info('Started thread that checks for send messages.')

	while True:
		logger.info('Checking for send messages...')
		while not sendMsgQueue.empty():
			msg = sendMsgQueue.get()
			logger.debug('Send message ' + msg + ' to ' + Comunication.peerName + '\'s TextServer.')
			s = Comunication.peerSocket
			s.send(msg)
		sleep(SLEEP_AMNT)
th = Thread(target = checkSendMsg)
th.start()

# Check for received text messages thread
def checkRcvMsg():
	logger.info('Started thread that checks for receive messages.')

	while True:
		logger.debug('Checking for receive messages...')
		while not rcvMsgQueue.empty():
			msg = rcvMsgQueue.get()
			logger.debug('Receive message ' + msg + ' from the ' + Comunication.peerName + '\'s TextServer.')
			# TODO write the received text message in the textWindow
		sleep(SLEEP_AMNT)
th = Thread(target = checkRcvMsg)
th.start()	

# Update online users thread

# GUI loop
root.mainloop()