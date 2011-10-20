import socket
from simplejson import loads

request = "GET / HTTP/1.1\r\nHOST: radiant-meadow-2958.herokuapp.com\r\n\r\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(('localhost', 8080))
sock.connect(('radiant-meadow-2958.herokuapp.com', 80))
sock.send(request)
data = sock.recv(1024)
print data

while len(data):
      data = sock.recv(1024).split('\r\n')[1]
      print loads(data)
sock.close()
