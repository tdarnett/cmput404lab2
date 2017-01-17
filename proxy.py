#!/usr/bin/env python
import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # This is how we reuse the port

server_socket.bind(('0.0.0.0', 7000)) # We must bind the port so other machines can connect
# We cannot use port 80 (or anything less that 1024) unless we are root
# ('0.0.0.0' means we are listening on any address)
server_socket.listen(5) # OS should listen up to 5 incoming connections in the queue, otherwise start rejecting


while True:
    (incoming_socket, address) = server_socket.accept() # wait for a connction and create another socket that is specific to the connection
    print "We got a connection from %s" % str(address)
    if os.fork() != 0:
        continue

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(("www.google.com", 80))

    incoming_socket.setblocking(0)
    client_socket.setblocking(0)

    while True:
        """
        This will read whatever the client is requesting and print it out
        """
        request = bytearray()
        while True:
            try:
                part = incoming_socket.recv(1024)
            except IOError as e:
                if e.errno == socket.errno.EAGAIN:
                    part = None
                else:
                    raise

            if part:
                client_socket.sendall(part)
                request.extend(part)
            else:
                break

        if len(request) > 0:
            print request

        response = bytearray()
        while True:
            try:
                part = client_socket.recv(1024)
            except IOError as e:
                if e.errno == socket.errno.EAGAIN:
                    part = None
                else:
                    raise

            if part:
                incoming_socket.sendall(part)
                response.extend(part)
            else:
                break

        if len(response) > 0:
            print response

#     Non blocking socket IO says 'dont pause on the receive lines'
