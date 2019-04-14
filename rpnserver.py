#!/usr/bin/python

# Author : Archit Bansal
# Username : abansal88
# GTID : 903396126

import socket
import sys

HOST = '127.0.0.1'
PORT = 65432

try:
    PORT = int(sys.argv[1])
except Exception as e:
    pass

# Create a TCP stream socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host address and the port number
s.bind((HOST, PORT))

# Start listening on the socket with a max of 5 parallel connections
s.listen(5)

# Keep accepting connections on the socket till an explicitly break is issued
while True:
    try:
        # Accepting a connection
        conn, addr = s.accept()
        # Keep reading the data from the socket upto a max of 
        # 1024 bytes and start processing the input
        while True:
            # On completion of the full postfix expression, the client closes 
            # the socket from its end and recv return 'None' in that case
            # This breaks the loop and the server also closes the connection from its side
            data = conn.recv(1024).decode()
            if not data:
                break
            print "Server received : ", data
            # Extract the operands and the operator from the client message
            expr = data.split(" ")
            op1 = float(expr[0])
            op2 = float(expr[1])
            operator = expr[2]
            retVal = 0
            # perform the required operation
            if operator == '+':
                retVal = op1 + op2
            elif operator == '-':
                retVal = op1 - op2
            elif operator == '*':
                retVal = op1 * op2
            elif operator == '/':
                retVal = op1 / op2
            # Return an error if a value overflow occurs
            if len(str(retVal)) > 1024:
                conn.sendall("error : overflow in the calculation")
            # Return the result in the happy case
            else:
                conn.sendall(str(retVal).encode())
        # Close the connection
        conn.close()
    # Catch any exception during the data processing and 
    # send it to the client before closing the connection
    # and continue listening on the port for more connections
    except Exception as e:
        print e
        conn.sendall("error " + str(e))
        conn.close()
        continue
# Close the socket before exiting the server
s.close()
