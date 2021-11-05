import socket
import jwt

s = socket.socket()

host = "192.168.43.157"
port = 12345
key = "secret"

def enterCommand():
    try:
        s.connect((host, port))

        while True:
            command = input("ssh: ")
            encodedCommand = jwt.encode({"command": command},key,algorithm= "HS256")
            print("Command encoded succesfully")
            s.send(encodedCommand.encode('utf-8'))

            if command == 'exit': break
        s.close()

    except socket.error as msg:
        print("[Server is not available] Message: ",msg)