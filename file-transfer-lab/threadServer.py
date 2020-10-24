
#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

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
import threading

files_being_transfered = []
lock = threading.Lock()

class Server(Thread):
	def __init__(self, sockAddr):
		Thread.__init__(self)
		self.sock, self.addr = sockAddr
		self.fsock = EncapFramedSock(sockAddr)

	def run(self):
		print("new thread handling connection from", self.addr)

		while True:
			lock.acquire()
			filename = self.fsock.receive(debug)
			if debug: print("rec'd: ", filename)
			if filename is None:     # done
				if debug: print("thread connected to {addr} done") #removed f here
				self.fsock.close()
				lock.release()
				return   
 
			filename = filename.decode()
			if filename in files_being_transfered:
				self.fsock.send("True", debug)	#remove b
			else:
				self.fsock.send("False", debug) #remove b
				files_being_transfered.append(filename)
				try:
					data = self.fsock.receive(debug)
				except:
					print("Unable to receive and finalize transfer... terminating transfer...")
					sys.exit(0)
				open_file = open(filename, 'wb')
				open_file.write(data)
				open_file.close()
				self.sock.shutdown(socket.SHUT_RD)
				self.sock.close()
		lock.release()

while True:
	sockAddr = lsock.accept()
	server = Server(sockAddr)
	server.start()
