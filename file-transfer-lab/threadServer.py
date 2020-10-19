
#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params

from os.path import exists

switchesVarDefaults = (
	(('-l', '--listenPort') ,'listenPort', 50001),
	(('-d', '--debug'), "debug", False), # boolean (set if present)
	(('-?', '--usage'), "usage", False), # boolean (set if present)
	)

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
	params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
	def __init__(self, sockAddr):
		Thread.__init__(self)
		self.sock, self.addr = sockAddr
		self.fsock = EncapFramedSock(sockAddr)
	def run(self):
		print("new thread handling connection from", self.addr)
		while True:
			payload = self.fsock.receive(debug)
			if debug: print("rec'd: ", payload)
			if not payload:     # done
				if debug: print("thread connected to {addr} done") #removed f here
				self.fsock.close()
				return          # exit
            # here
			payload = payload.decode()
			if exists(payload):
				self.fsock.send("True", debug)	#remove b
			else:
				self.fsock.send("False", debug) #remove b
				try:
					payload2 = self.fsock.receive(debug)
				except:
					print("Unable to receive and finalize transfer... terminating transfer...")
					sys.exit(0)
			#	if no payload2:
			#		break
				payload2 += b"!"
				try:
					self.fsock.send(payload2, debug)
				except:
					print("Unable to receive and finalize transfer... terminating transfer...")
				rcvd_file = open(payload, 'wb')
				rcvd_file.write(payload2)
				rcvd_file.close()

while True:
	sockAddr = lsock.accept()
	server = Server(sockAddr)
	server.start()
