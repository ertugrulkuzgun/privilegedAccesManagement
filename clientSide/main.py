import socket
import jwt               
from sshCommand import enterCommand

# creating socket
s = socket.socket()          

host = "192.168.43.157"
port = 12345
key = "secret"                

try:
    # Connection
    s.connect((host, port)) 
    username = input("Enter username: ")
    password = input("Enter password: ")
    encoded = jwt.encode({"username": username, "password": password}, key, algorithm="HS256")
    print(encoded)
    s.send(encoded.encode('utf-8'))
    # close connection
    s.close()

    enterCommand()

except socket.error as msg:
    print("[Server is not available.] Message:", msg)