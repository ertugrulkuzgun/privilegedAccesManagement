import socket
import jwt               
from sshCommand import enterCommand
import sys

def sendData (sock:socket, data:str):
    """
    Send data to the client using socket 'sock'
    """
    try :
        sock.send(data.encode('utf-8'))
    except socket.error as e :
        print("Error sending data: %s" %e)
        sys.exit(1)

def recvData (sock, size):
    """
    Receive data of size 'size' from the client using socket 'sock'
    """
    try :
        data = sock.recv(size)
    except socket.error as e :
        print("Error receiving data: %s" %e)
        sys.exit(1)

    return data

def sendProcessID(host,port,processID):
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e :
        print("Error creating server socket: %s" %e)
        sys.exit(1) 
    s.connect((host,port))
    sendData(s,processID)
    s.close()

def sendCredentials(host,port):
    key = "secret"
    processID = "1"
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e :
        print("Error creating server socket: %s" %e)
        sys.exit(1) 

    sendProcessID(host,port,processID)

    try:
        s.connect((host, port))
    except socket.gaierror as e:
        print("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print("Connection Error: %s" %e)
        sys.exit(1)
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    encoded = jwt.encode({"username": username, "password": password}, key, algorithm="HS256")
    print(encoded)
    sendData(s,encoded)
    s.close()
    print('connection closed') 

def sendCommand(host,port):
    key = "secret"
    processID = "2"
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e :
        print("Error creating server socket: %s" %e)
        sys.exit(1)

    sendProcessID(host,port,processID)

    try:
        s.connect((host, port))
    except socket.gaierror as e:
        print("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print("Connection Error: %s" %e)
        sys.exit(1)
    command = input("SSH: ")
    encodedCommand = jwt.encode({"command": command,},key,algorithm= "HS256")
    print("Command encoded succesfully")
    sendData(s,encodedCommand)
    s.close()
## I stay here
def getUserAvailability(sock:socket)->str:
    conn,addr = sock.accept()
    sock.settimeout(None)
    print('Got connection from',addr)
    userAvailability = recvData(conn,size=1024)
    decodedUserAvailability = userAvailability.decode('utf-8')


# creating socket
def main():
    #•s = socket.socket()          

    host = "192.168.43.157"
    port = 12348
    
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e :
        print("Error creating server socket: %s" %e)
        sys.exit(1)

    try :
        s.bind((host, port))
    except socket.error as e :
        print("Error in binding host and port: %s" %e)

    sendCredentials(host,port)
    getUserAvailability(s)
    sendCommand(host,port)
    
                

    """ try:
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
        print("[Server is not available.] Message:", msg) """

main()