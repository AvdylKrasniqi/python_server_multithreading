import socket

SERVER = input("Shkruani HOST te server (by default: localhost): ")
if(SERVER == ""):
  SERVER = "localhost"

PORT = input("Shkruani PORT te server (by default: 13000): ")
try:
  PORT = int(PORT)
except Exception as e:
  PORT = 13000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes("connectiontest",'UTF-8'))
while True:
  in_data =  client.recv(1024)
  print("Pergjigjja:" ,in_data.decode())
  out_data = input()
  if out_data=='':
    out_data = "unknowncommand"
  client.sendall(bytes(out_data,'UTF-8'))
  if out_data=='exit':
    break
client.close()