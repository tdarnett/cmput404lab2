#!/usr/bin/env python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET indicates that we want an IPV4 socket
# socket.AF_STREAM indicates that we want an TCP socket

client_socket.connect(('www.google.ca', 80)) # Tuple because C uses structures
# note that there is no http:// (because this is so low level and we are doing the protocol ourselves)
# port 80 is the standard http port

request = 'GET / HTTP/1.0\r\n\r\n'
# a blank line in http will separate headers and the body

client_socket.sendall(request)


"""
This is a loop that says we will do a recieve of up to 1kb, and if we get it then we keep reading.
We must read it in until all bytes are read
"""
response = bytearray()
while True:
    part = client_socket.recv(1024)
    if part:
        response.extend(part)
    else:
        break

print response
