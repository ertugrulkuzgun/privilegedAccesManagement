import socket
import jwt

testUsername = "ertu"
testPassword = "130245"

def receiveCommands(s: socket,k)-> str:
    c = s.accept()[0]
    command = c.recv(1024)
    decodedCommand = jwt.decode(command,k,algorithms="HS256")
    plainCommand = decodedCommand.get('command')
    print(plainCommand)
    c.close()
    return plainCommand

def main():
    host = "192.168.43.157"
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

    c, addr = s.accept()
    print("Coming connection: ", addr)

    credentials = c.recv(1024)
    print(credentials)
    decoded = jwt.decode(credentials, key, algorithms="HS256")
    username = decoded.get('username')
    password = decoded.get('password')
    print(decoded)
    print(username + " " + password)

    if username == testUsername and password == testPassword:
        receiveCommands(s,key)

    else:
        errMsg = c.send("Wrong credentials.")
        c.close()

    c.close()



main()

    
