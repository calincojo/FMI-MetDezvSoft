import socket
import sys
import atexit
import signal
from tempfile import mkstemp
from shutil import move
from os import remove, close, path

namedb = {}
with open('namedb', 'r') as f:
	for line in f.readlines():
		name = line.split(' ')[0]
		ip = line.split(' ')[1]
		namedb[name] = ip

try:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except socket.error, msg:
		print 'Failed to create socket. Error Code: ' + str(msg[0]) + ', Error Message: ' + str(msg[1])
		sys.exit();

	'''
	def exit_handler():
		cleanup()
		sys.exit(0)
	atexit.register(exit_handler)

	def signal_handler(signal, frame):
		cleanup()
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	'''
	print 'Socket created.'

	s.bind(('', 1234))
	s.listen(1)

	while 1:
		print '\nWaiting requests...'
		(c, addr) = s.accept()

		print 'Request from ', addr

		msg = c.recv(1024)
		#ip = msg.split(' ')[2].strip()
		ip = addr[0]
		op = msg.split(' ')[0].strip()
		name = msg.split(' ')[1].strip()

		if op == 'add':
			entry = name + ' ' + ip + '\n'
			if namedb.has_key(name):
				# if the name already exists in the db then search for it and update it in namedb
				fh, abs_path = mkstemp()
				with open(abs_path, 'w') as new_file:
					with open('namedb', 'r') as old_file:
						for line in old_file.readlines():
							old_name = line.split(' ')[0]
							if old_name == name:
								new_file.write(entry)
							else:
								new_file.write(line);
				close(fh);
				remove('namedb')
				move(abs_path, 'namedb')
				print 'Update namedb file with modified entry ' + entry
			else:
				# if the name is new then update the db file
				with open('namedb', 'a') as f:
					f.write(entry)
					print 'Update namedb file with new entry ' + entry
			namedb[name] = ip
		elif op == 'lookup':
			if namedb.has_key(name):
				c.send(str(namedb[name]))
			else:
				c.send('null')
		c.close()
finally:
	s.close()
	print 'Socket closed'