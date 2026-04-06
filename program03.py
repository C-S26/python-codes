#check open ports in machine
import socket 

s = socket.socket()
s.settimeout(5)

result = s.connect_ex(("127.0.0.1", 8081))

if result ==0:
    print("open")
else:
    print("closed")

s.close()