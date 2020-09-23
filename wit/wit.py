#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import socket
import struct

# Function to convert   
def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s)) 

# ip address of IC-705 connected to WiFi
tcp_ip = '10.155.0.157'
# standard tcp port for this transsmision
tcp_port = 60000 

# open test.jpg
f = open("test.jpg", 'rb')
f.seek(0,2)
file_size = f.tell().to_bytes(3, byteorder='big')
f.seek(0)

command = b'\x01\x00\x00\x00\x00\x04\x00\x00\x00' # command for file transfer to radio
cmd_ack = b'\x01\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00' # command acknowledge
rcv_ack = b'\x01\x02\x00\x00\x00\x02\x00\x00\x04\x00' # receive acknowledge
send_next = b'\x01\x03\x00\x00\x04\x03\x00\x00\x01' # header of next part of picture
send_last = b'\x01\x03\x00\x00\x00\x74\x00\x00\x01' # header of last part of picture

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((tcp_ip, tcp_port))
message_tmp = command + file_size
s.send(message_tmp)
s.setblocking(1)

data = s.recv(22)
answer = cmd_ack + rcv_ack

if(data == cmd_ack):
	data = s.recv(22)
	if(data != rcv_ack):
		print("No 'receive ack' received from radio")
		exit()
elif(data != answer):
	if(data != cmd_ack):
		print("No 'command ack' received from radio")
		print(data)
		exit()

while True:
	piece = f.read(1024)  
	if not piece:
		break
	piece_size = len(piece).to_bytes(2, byteorder='big')
	if(len(piece)==1024):
		to_send = send_next + piece_size + piece
		s.send(to_send)
		data = s.recv(10)
		while (len(data) == 0):
			data = s.recv(10)
		if(data != rcv_ack):
			print("Error, 'receive ack' not received.")
			exit()
	else:
		to_send = send_last + piece_size + piece
		s.send(to_send)
f.close()
s.close()
