#!usr/bin/env python3

import socket
import os
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(),50001))
print("Connected...")
new_data = True

while True:
	if new_data:
		filename = input(str("Please enter filename for incoming transfer: ")
		data_file = open(filename, "wb")
		new_data = False

	while True:
		data = s.recv(1024)
		
		while True:
			if not data:
				new_data = True
				break
			data_file.write(data)
			data = s.recv(1024)

		data_file.close()
