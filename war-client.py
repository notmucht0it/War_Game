"""
Kevin Monahan
CompSci 520 - Homework 3
10/30/2023
War Client
"""
import socket
PORT = 4444

client_socket = socket.socket()  # instantiate
client_socket.connect(("127.0.0.1", PORT))  # connect to the server

client_socket.close()  # close the connection
