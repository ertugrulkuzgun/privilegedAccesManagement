import socket
import jwt
import sys

testUsername = "ertu"
testPassword = "130245"

def sendData (sock, data:str):
    """
    Send data to the server using socket 'sock'
    """
    try :
        sock.send(data.encode('utf-8').decode('utf-8'))
    except socket.error as e :
        print("Error sending data: %s" %e)
        sys.exit(1)

def recvData (sock, size):
    """
    Receive data of size 'size' from the server using socket 'sock'
    """
    try :
        data = sock.recv(size)
        print(data)
        #decodedData = data
    except socket.error as e :
        print("Error receiving data: %s" %e)
        sys.exit(1)
    
    return data

def receiveCommands(s: socket,k)-> str:
    #s.listen(5)
    while True:
        conn,addr = s.accept()
        s.settimeout(None)
        print('Got connection from', addr)
        command = recvData(conn,size=1024)
        decodedCommand = jwt.decode(command,k,algorithms="HS256")
        plainCommand = decodedCommand.get('command')
        if plainCommand == "exit":
            conn.close()
            #sys.exit(1)
            break
        print(plainCommand)
        
        return plainCommand

def getCredentials(s: socket):
    key = "secret"
    conn,addr = s.accept()
    s.settimeout(None)
    print('Got connection from', addr)
    encodedCredentials = recvData(conn,size=1024)
    print(encodedCredentials)
    decoded = jwt.decode(encodedCredentials, key, algorithms="HS256")
    username = decoded.get('username')
    password = decoded.get('password')
    print(decoded)
    print(username + " " + password)
    conn.close()
    return username,password

def getProcessID(s: socket)->str:
    conn,addr = s.accept()
    s.settimeout(None)
    print('Got connection from',addr)
    processID = recvData(conn,size=1024)
    decodedProcessID = processID.decode('utf-8')
    print(decodedProcessID)
    conn.close()
    return decodedProcessID

def sendWrongCredentialsInfo(host,port):
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e :
        print("Error creating server socket: %s" %e)
        sys.exit(1)
    
    try:
        s.connect((host, port))
    except socket.gaierror as e:
        print("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print("Connection Error: %s" %e)
        sys.exit(1)

    msg = "Wrong credentials. Connection will close"
    sendData(s,msg)
    s.close()

def main():
    host = "192.168.43.157"
    port = 12348
    key = "secret"

    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e :
        print("Error creating server socket: %s" %e)
        sys.exit(1)

    try :
        s.bind((host, port))
    except socket.error as e :
        print("Error in binding host and port: %s" %e)

    s.listen(5)
    ######################
    #c, addr = s.accept()
    #print("Coming connection: ", addr)

    while True:
        processID = getProcessID(s)
        print(processID)
        if processID == "1":
            credentials = getCredentials(s)
            
        if processID == "2":
            if credentials[0] == testUsername and credentials[1] == testPassword:
                while True:
                    returnValue = receiveCommands(s,key)
                    print(returnValue)
                    if returnValue == "exit": break
            else:
                s.close()


    
    #c.close()

    

   """  #else:
        errMsg = c.send("Wrong credentials.")
        print(errMsg)
        c.close() """

    



main()

    
