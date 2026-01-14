# the purpose of this server is to keep track of
# Guest ID
# Whether or not they already have a FP
# The time at which they last obtained a FP

#and some server specific things such as
# Maximum number of FPs to be held by a given person at a time

import socket
import select
from tinydb import TinyDB, Query
import sys

GUESTS = TinyDB('guests.json')

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8067

DEBUG_HOST = "127.0.0.1"
DEBUG_PORT = 8069

MAXFP = 1
WAITTIME = -1

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((SERVER_HOST, SERVER_PORT))

debugSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
debugSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
debugSocket.bind((DEBUG_HOST, DEBUG_PORT))

serverSocket.listen(5)
debugSocket.listen(5)


inputs = [serverSocket, debugSocket]

outputs = []

#################################################################################

def validateFastpass(guestID):
    return True

def processRequest(request):
    tokens = request.split("/")
    
    Guest = Query()
    
    guest = GUESTS.search(Guest.guestID == int(tokens[2]))
    
    print(guest)
    
    return "message recieved"

#################################################################################

while inputs:

    # Wait for at least one of the sockets to be ready for processing
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    for s in readable:
        if s is serverSocket:
            conn, addr = s.accept()
            conn.setblocking(0)
            inputs.append(conn)
            print("Connected by ride")
            
        elif s is debugSocket:
            conn, addr = s.accept()
            inputs.append(conn)
            print("Connected by admin")
            
        else:
            data = s.recv(1024)
            portnum = s.getsockname()[1]
            print(str(portnum))
            if data:
                message = data.decode('UTF-8')
                response = "Bad Request"
                
                try:
                    response = processRequest(message)
                except Exception as e:
                    print("Bad Request...")
                    
                conn.sendall(response.encode('utf-8'))    
                
            else:
                inputs.remove(s)
                s.close()