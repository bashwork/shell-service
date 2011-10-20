import socket
from simplejson import loads

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))
#sock.connect(('radiant-meadow-2958.herokuapp.com', 8080))
sock.send("GET / HTTP/1.1\r\n\r\n")
data = sock.recv(1024)
print data

while len(data):
      data = sock.recv(1024).split('\r\n')[1]
      print loads(data)
sock.close()
