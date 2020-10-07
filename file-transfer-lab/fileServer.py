#!usr/bin/env python3

import socket
import os
import sys

#os.fork()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),50001))
s.listen(1)

while True:
	print("Waiting for incoming connections...")
	conn, addr = s.accept()
	print(addr, "has connected to the server")
	
	filename = input(str("Please enter the filename for transfer: "))
	data_file = open(filename, "rb")
	print("Sending ", filename)
	data = data_file.read(1024)

	while data:
		conn.send(data)
		data = data_file.read(1024)
	
	data_file.close()
	print("Data transmitted successfully")
	conn.shutdown(socket.SHUT_WR)
	conn.close()
	
