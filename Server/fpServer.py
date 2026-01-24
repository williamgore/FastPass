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
import time

GUESTS = TinyDB('guests.json')

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8067

DEBUG_HOST = "127.0.0.1"
DEBUG_PORT = 8069

MAXFP = 1       #the maximum number of fastpasses to be held at a given time
WAITTIME = 1000    #the amount of time you must wait before recieving an additional fast pass - measured in minutes

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
    print(request)
    
    Guest = Query()
    
    tokens = request.split("/")
    #tokens[1] is our method
    if tokens[1] == 'new':
        
        
        guest = (GUESTS.search(Guest.guestID == int(tokens[2])))[0]
        
        #a guest can recieve a fast pass if:
        # their current number of fastpasses is less than the maximum
        # AND the time since their last fastPass is less than WAITTIME
        
        print(guest)
        
        print("has fast pass: " + str(guest['hasFP']))
        
        if int(guest['hasFP']) < MAXFP:
            if (time.time() - int(guest['lastFP']))/60 > WAITTIME:
                print(guest['name'] + " can recieve a fastpass")
    
    # this method is called by the client upon successful distribution of the FastPass
    elif tokens[2] == 'add':
        ride = tokens[0]
        
        GUESTS.update({'ride': ride}, Guest.guestID == int(tokens[2]))
        
        GUESTS.update({'hasFP': ride}, Guest.guestID == int(tokens[2]))
        print()
    
    elif tokens[3] == 'redeem':
        print()
        
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
                response = "Bad Request\nExpecting GuestID as sole input"
                
                try:
                    response = processRequest(message)
                except Exception as e:
                    print("Bad Request...")
                    
                conn.sendall(response.encode('utf-8'))    
                
            else:
                inputs.remove(s)
                s.close()