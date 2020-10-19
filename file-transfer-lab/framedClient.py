#! /usr/bin/env python3

# Echo client program
import socket, sys, re

from os.path import exists

sys.path.append("../lib")       # for params
import params

from encapFramedSock import EncapFramedSock

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
	(('-s', '--server'), 'server', "127.0.0.1:50001"),
	(('-d', '--debug'), "debug", False), # boolean (set if present)
	(('-?', '--usage'), "usage", False), # boolean (set if present)
	)

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
	params.usage()

try:
	serverHost, serverPort = re.split(":", server)
	serverPort = int(serverPort)
except:
	print("Can't parse server:port from '%s'" % server)
	sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

sock = socket.socket(addrFamily, socktype)

if sock is None:
	print('could not open socket')
	sys.exit(1)

sock.connect(addrPort)

filename = input("Please enter name of file to send: ")

if exists(filename):
	open_file = open(filename, 'rb')
	data = open_file.read()
	open_file.close()
	if len(data) == 0:
		print("File is empty... terminating transfer...")
		sys.exit(0)
	else:
		server_filename = input("Please enter name for the file on transmitted server: ")
		framedSend(sock, server_filename.encode(), debug)
		file_exists = framedReceive(sock, debug)
		file_exists = file_exists.decode()
		if file_exists == "True":
			print("Invalid filename... terminating transfer...")
			sys.exit(0)
		else:
			try:
				framedSend(sock, data, debug)
			except:
				print("Unable to secure transfer... terminating transfer...")
				sys.exit(0)
			try:
				framedReceive(sock, debug)
			except:
				print("Unable to secure transfer... terminating transfer...")
				sys.exit(0)
else:
	print("Cannot transfer non-existant file... terminating transfer...")
	sys.exit(0)
