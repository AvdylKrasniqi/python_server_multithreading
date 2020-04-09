import socket
import sys

HOST = input("Shkruani HOST te server (by default: localhost): ")
if(HOST == ""):
  HOST = "localhost"

PORT = input("Shkruani PORT te server (by default: 13000): ")
try:
  PORT = int(PORT)
except Exception as e:
  PORT = 13000


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



while True:
  out_data = input("Shkruani kerkesen: ")
  if out_data=='':
    out_data = "unknowncommand"
  sock.sendto(bytes(out_data + "\n",'UTF-8'), (HOST, PORT))
  if out_data=='exit':
    break
  received = sock.recv(1024)
  print("Pergjigjje " ,received.decode())