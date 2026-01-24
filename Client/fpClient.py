#this is the file that attractions offering fast pass will have running

#each attraction must:
    # have its own service rate √
    # have its own name √
    # keep track of its own distributed fast pass
    # validate distributed fast passes
    # calculate fast pass return times (1 hour window)
    # have a 'down time' mode
    # OPTIONAL:
    # have a fast pass return option (this would require tracking fast pass IDs)


import socket
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8067

SERVICE_RATE = 100 # Measured in guests per hour
NAME = "New Ride"

#checking for command line arguments
try:
    NAME = sys.argv[1]
except Exception as e:
    print("No name given, using default name of " + NAME)
try:
    SERVICE_RATE = sys.argv[2]
except Exception as e:
    print("No service rate given, using default service rate of " + str(SERVICE_RATE))

FP_DIST = 0

#formatting
FPWIDTH = 21
NAMELINE = NAME
spaces = (FPWIDTH - len(NAME))/2
for i in range(int(spaces)):
    NAMELINE = " " + NAMELINE + " "

FASTPASSPRINT = '''
#####################
#{}#
#####################
#     FAST PASS     #
#   Please Return   #
#  Anytime Between  #
#      {}     #
#        AND        #
#      {}     #
#
#     IMPORTANT:    #
#    You may only   #
#   have one valid  #
#  FASTPASS ticket  #
#     at a time     #
#####################
'''

# first  {} = centered ride name
# second {} = return window begin time "##:## #M"
# third  {} = return window end time   "##:## #M"

INVALIDFASTPASS = '''
#####################
#{}#
#####################
#                   #
#    NOT A VALID    #
#  FASTPASS TICKET  #
#  Anytime Between  #
#                   #
#   You currently   #
#  hold an active   #
# FASTPASS® ticket  #
#       for         #
#{}#
#                   #
# Another FASTPASS® #
#  ticket will be   #
#  available after  #
#      {}     #
#####################
'''

# first  {} = centered ride name
# second {} = fastpass availability time "##:## #M"

# When a fast pass is reqested, take the guestID and send it to the server
# the server will send one of two things
    # A message saying the guest can receive a fast pas
    # OR
    # A message saying the guest cannot receive a fast pass,
    # The attration they already have a fast pass for
    # And the time at which they can receive a new fast pass
    
# in the case of a fast pass being given to the guest, print the fast pass, then
# send another message back to the server with the information on the fast pass that
# the guest received (this could be condensed into one step, but what if the machine malfunctions?)


#####################
# FAST PASS PRINTER #
#####################

def printer(valid) :
    if valid:
        print("Valid")
    else:
        print("Invalid")
#the two types of fastpasses need to be stored client side in case the server goes down

#############################
# FAST PASS REQUEST HANDLER #
#############################


    
running = 1
    
while running:

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #the client should have two input methods
        # new (guestID)
        # redeem (guestID)
        message = input("\nInput your request (new/redeem) and your guestID, separated by a space:\n")
        
        serverSocket.connect((SERVER_HOST, SERVER_PORT))
        
        if message == "quit":
            running = 0
            serverSocket.close()
        else:
            tokens = message.split()
            message = NAME + "/" + tokens[0] + "/" + tokens[1]
            serverSocket.sendall(message.encode('utf-8'))
            response = serverSocket.recv(1024)
            print(response.decode('utf-8'))
            
    except Exception as e:
        print("Unable to connect to server, assuming honest guest...")
        print(e)
        
    
        
print("Exiting the program...")