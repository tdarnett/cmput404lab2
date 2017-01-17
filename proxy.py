#!/usr/bin/env python
import socket
import os, select

# from joshua2ua github (repo: cmput404w17lab2) https://github.com/joshua2ua/cmput404w17lab2/blob/master/proxy.py on Jan 17, 2017

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # This is how we reuse the port

server_socket.bind(('0.0.0.0', 7002)) # We must bind the port so other machines can connect
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
            elif part is None:
                break
            else:
                exit(0)

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
            elif part is None:
                break
            else:
                exit(0)

        if len(response) > 0:
            print response

        # fixes busy waiting problem
        select.select(
            [incoming_socket, client_socket], # read
            [], # write
            [incoming_socket, client_socket], # exceptions
            1.0 # timeout
        )

#     Non blocking socket IO says 'dont pause on the receive lines'
