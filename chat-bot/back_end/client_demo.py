#!/usr/bin/env python3
import sys
import socket

args = sys.argv[1:]
ip = '127.0.0.1'  # The server's hostname or IP address
port = int(args[0])        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    for l in sys.stdin:
        s.send(l.encode())
        #print("sent",l)
        data = s.recv(1024).decode()
        print(data)       


