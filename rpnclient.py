#!/usr/bin/python

# Author : Archit Bansal
# Username : abansal88
# GTID : 903396126

import socket
import sys
import re

HOST = '127.0.0.1'

# This function checks if the token is a valid operator or not
# Return True if valid, False otherwise
def isOperator(ch):
	return ch == '+' or ch == '-' or ch == '*' or ch == '/'

# This function checks of the token is a valid operand or not (A valid float/int value)
# Return True if valid, False otherwise
def isOperand(inp):
	try:
		temp = float(inp)
	except Exception as e:
		return False
	return True

# This function checks if the given expression is a valid postfix expression or not
# Return True if valid, False otherwise
def validate_expr(EXPR):
	earr = EXPR.split(" ")
	counter = 0
	for item in earr:
		if isOperator(item) == False and isOperand(item) == False:
			print "unrecognised input : ", item
			exit()
		if isOperator(item) == False:
			counter += 1
		else:
			counter -= 2
			if counter < 0:
				print "please give a valid postfix expression : ", EXPR
				exit()
			counter += 1
	if counter != 1:
		print "please give a valid postfix expression : ", EXPR
		exit()

# The main starts
if __name__ == '__main__':
	# Read port and postfix expression from the cmd
	try:
		PORT = int(sys.argv[1])
	except Exception as e:
		print "port number not provided : ", e
		exit()

	try:
		EXPR = sys.argv[2]
	except Exception as e:
		print "expression to evaluate not provided : ", e
		exit()

	# Validate the length of the postfix expression
	if len(EXPR) > 1024:
		print "too long an expression : max length allowed is 1024"
		exit()

	# Remove extra spaces from the expression
	EXPR = re.sub(' +', ' ', EXPR).strip()

	# Validate the expression
	validate_expr(EXPR)

	inarr = EXPR.split(" ")
	stack = []

	# Create the TCP socket to talk to the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		# Connect to the server host and port
		s.connect((HOST, PORT))
	except Exception as e:
		print "error while connecting to the server : ", e
		exit()
	try:
		# Process the postfix expression and invoke the server for computations one at a time, 
		# saving the result of each step and storing in a stack
		for index, item in enumerate(inarr):
			if isOperator(item) == True:
				operand2 = stack.pop()
				operand1 = stack.pop()
				if float(operand2) == 0 and item == '/':
					raise Exception("error in the input : divide by zero encountered")
				data = str(operand1) + " " + str(operand2) + " " + item
				s.sendall(data.encode())
				data = s.recv(1024)
				data = data.decode()
				# Checking for error from the server
				if "error" in data:
					raise Exception("error from the server : ", data)
				stack.append(data)
				if index == len(inarr)-1:
					print "Client received final : ", data.decode()
				else:
					print "Client received : ", data.decode()
			else:
				stack.append(item)
		# Close the socket when whole postfix expression is evaluated
		s.close()
	except Exception as e:
		# Catch any exception that might have happened during the processing 
		# and calling the server. Close the socket and exit the program
		print "error while sending/receiving data to the server : ", e
		s.close()
		exit()
