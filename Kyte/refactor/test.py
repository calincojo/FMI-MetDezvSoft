import unittest
import subprocess
import socket
import runpy

class NamingServiceAPI(unittest.TestCase):
	serviceProc = None

	@staticmethod
	def sendQuery(query):
		s = socket.socket()
		s.connect((socket.gethostname(), 1234))
		s.send('')
		s.close()

	def setUp(self):
		#NamingServiceAPI.serviceProc = subprocess.Popen(['python', 'namingServiceServer.py'])
		pass
	def tearDown(self):
		#NamingServiceAPI.serviceProc.kill()
		pass
	def testAdd(self):
		NamingServiceAPI.sendQuery('add test')
	def testLookup(self):
		NamingServiceAPI.sendQuery('lookup test')
	def testAddWrong(self):
		NamingServiceAPI.sendQuery('add test test2')
	def testEmptyQuery(self):
		NamingServiceAPI.sendQuery('')
	def testRandom(self):
		NamingServiceAPI.sendQuery('Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...')

unittest.main()