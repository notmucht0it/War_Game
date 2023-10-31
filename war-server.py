"""
Kevin Monahan
CompSci 520 - Homework 3
10/30/2023
War Server
"""
import socket
PORT = 4444

server_socket = socket.socket()
server_socket.bind(("127.0.0.1", PORT))
server_socket.listen(3)
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))

conn.close()  # close the connection
