import socket
import sys
import getpass

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print '[ERROR] Failed to create socket'
	sys.exit()

host = 'localhost' #change to 10.0.0.4 when using on mininet 
port = 2839

while 1:
	print 'Enter username:'
	msg = raw_input('>: ')
	try:
		packet = '0' + msg
		s.sendto(packet, (host, port))
		d = s.recvfrom(1024)
		reply = d[0]
		if reply[0] == '0':
			break
		elif reply[0] == '1':
			print 'Account already in use on another device'
		else:
			print 'Username does not exit'
	except socket.error:
		print '[ERROR] Socket transmission failed'
		sys.exit()
while 1:
	print 'Enter password:'
	msg = getpass.getpass('>: ')
	try:
		s.sendto('1' + msg, (host, port))
		d = s.recvfrom(1024)
		reply = d[0]
		if reply == '0':
			print 'Login successful'
			break
		elif reply == '1':
			print 'Account already in use on another device'
			sys.exit()
		else:
			print 'Incorrect password'
	except socket.error:
		print '[ERROR] Socket transmission failed'
		sys.exit()
s.sendto('8', (host, port))
d = s.recvfrom(1024)
reply = d[0]
print 'You have ' + reply + ' messages.'
while 1:
	print '[Menu]'
	print 'Select an action:'
	print '[1] Change Password'
	print '[2] Logout'
	print '[3] Send Message'
	print '[4] Broadcast Message'
	print '[5] Read Messages'

	msg = raw_input('>: ')

	if msg == '1':
		print 'Enter old password:'
		msg = getpass.getpass('>: ')
		try:
			s.sendto('1' + msg, (host, port))
			d = s.recvfrom(1024)
			reply = d[0]
			if reply == '2':
				print 'Incorrect password'
			else:
				print 'Input new password:'
				msg = getpass.getpass('>: ')
				s.sendto('2' + msg, (host, port))
				d = s.recvfrom(1024)
				reply = d[0]
				if reply == '0':
					print 'Password successfully changed'
		except socket.error:
			print '[ERROR] Socket transmission failed'
			sys.exit()

	elif msg == '2':
		try:
			s.sendto('3', (host, port))
			d = s.recvfrom(1024)
			reply = d[0]
			if reply == '0':
				print 'Logging out'
				break
		except socket.error:
			print '[ERROR] Socket transmission failed'
			sys.exit()

	elif msg == '3':
		print 'Select user'
		msg = raw_input('>: ')
		try:
			s.sendto('4' + msg, (host, port))
			d = s.recvfrom(1024)
			reply = d[0]
			if reply == '0':
				print 'Input message'
				msg = raw_input('>: ')
				s.sendto('5' + msg, (host, port))
				d = s.recvfrom(1024)
				reply = d[0]
				if reply == '0':
					print 'Message successfully sent'
				else:
					print 'Message failed to send'
			else:
				print 'User does not exist'
		except socket.error:
			print '[ERROR] Socket transmission failed'
			sys.exit()

	elif msg == '4':
		print 'Input Message'
		msg = raw_input('>: ')
		try:
			s.sendto('6' + msg, (host, port))
			d = s.recvfrom(1024)
			reply = d[0]
			if reply == '0':
				print 'Broadcast successfully sent'
			else:
				print 'Broadcast failed to send'
		except socket.error:
			print '[ERROR] Socket transmission failed'
			sys.exit()

	elif msg == '5':
		s.sendto('7', (host, port))
		d = s.recvfrom(1024)
		reply = d[0]
		if reply[0] == '0':
			print reply[1:]
		else:
			print '[Messages] No Messages'

	else:
		print 'Invalid input'
