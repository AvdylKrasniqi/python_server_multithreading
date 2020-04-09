import socket
import sys

HOST, PORT = "localhost", 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
  out_data = input()
  sock.sendto(bytes(out_data + "\n",'UTF-8'), (HOST, PORT))
  if out_data=='exit':
    break
  received = sock.recv(1024)
  print("From Server " ,received.decode())