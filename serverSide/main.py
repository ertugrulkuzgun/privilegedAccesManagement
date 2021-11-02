import socket
import jwt

host = "127.0.0.1"
port = 12345
key = "secret"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket creation successfull")

    s.listen(5)
    print("Socket listening")

except socket.error as msg:
    print("Hata :",msg)

while True:
    c, addr = s.accept()
    print("Coming connection: ", addr)

    message = c.recv(1024)
    print(message)
    decoded = jwt.decode(message, key, algorithms="HS256")
    username = decoded.get('username')
    password = decoded.get('password')
    print(decoded)
    print(username + password)

    c.close()