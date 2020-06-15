import socket
import select
import sys
import pickle
import ast
import FSNObjects
import traceback
import time
import platform
import threading
from threading import RLock
import copy
import FSFileHandler
from abstract.RaceFormat import RaceFormat
import sys


def versionIs3():
    is3 = False
    if (sys.version_info > (3, 0)):
        is3 = True
    return is3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
delim = b'\x1E'
# takes the first argument from command prompt as IP address
IP_address = socket.gethostname()

# takes second argument from command prompt as port number
port = input("Please input the port you'd like to use (or press return for default): ")
if(str(port)==""):
    port = 50002
else:
    port = int(port)

print("admin selected port "+str(port))

serverName = "noobs only"

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
print("binding to "+str(IP_address)+":"+str(port))
server.bind((IP_address, port))


"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

clientStates = {}
clientConnections = {}
outboundMessages = []
clientThreads = []

lock = RLock()

#let's ask the user which map they'd like
if versionIs3():
    mapFileName = input("Please input map file name: ")
else:
    mapFileName = str(raw_input("Please input map file name:"))
if(mapFileName==""):
    mapFileName = "The Shrine.fmp"



#let's ask the user which game mode they'd like
#gameModeList = [FSNObjects.MULTIPLAYER_MODE_1V1,FSNObjects.MULTIPLAYER_MODE_TEAM]
#gameModes = {0:"Free For All", 1: "Team Race"}
#gameModeString = ""
#for index in gameModes:
#    mode = gameModes[index]
#    gameModeString += str(index)+": "+mode+"\n"
#gameModeString += "Please input game mode: "
#gameModeSelection = int(input(gameModeString))
#gameMode = gameModeList[gameModeSelection]

#Let's ask the user what ranking will be based on
raceFormatString = ""
raceMetrics = {0:{"name":"First to X laps","format": RaceFormat.FORMAT_FIRST_TO_LAPS}, 1:{"name":"Most laps in time limit","format": RaceFormat.FORMAT_MOST_LAPS}, 2:{"name":"Fastest X, consecutive laps","format": RaceFormat.FORMAT_FASTEST_CONSECUTIVE}}
for index in raceMetrics:
    metric = raceMetrics[index]
    name = metric['name']
    raceFormatString += str(index)+": "+name+"\n"

raceFormatString += "Please enter the scoring metrics in the sequence of their importance (E.G. 132): "
if versionIs3():
    formatSelection = str(input(raceFormatString))
else:
    formatSelection = str(raw_input(raceFormatString))
raceFormatPriority = [raceMetrics[int(formatSelection[0])]['format'],raceMetrics[int(formatSelection[1])]['format'],raceMetrics[int(formatSelection[2])]['format']]

#let's ask what the lap limit should be
lapLimit = int(input("Please enter the lap limit: "))

#let's ask what the time limit should be
timeLimit = int(input("Please enter the time limit (in seconds): "))

#let's ask what the time limit should be
xConLaps = int(input("Number of consecutive laps for fastestXCon (1 for fastest single lap): "))

raceFormat = RaceFormat(raceFormatPriority,timeLimit,lapLimit,xConLaps)
formatContent = {"raceFormatPriority":raceFormatPriority,"timeLimit":timeLimit,"lapLimit":lapLimit,"consecutiveLapCount":xConLaps}

#let's load the map
mapContents = FSFileHandler.FileHandler().getMapContents(mapFileName)
runEvent = threading.Event()
runEvent.set()

def serverThread(a,b,runEvent):
    lastSend = time.perf_counter()
    while runEvent.is_set():
        #if(time.perf_counter()-lastSend > 0.016):
        if(time.perf_counter()-lastSend > 0.0):
            lastSend = time.perf_counter()
            sendPlayerUpdates()


def clientThread(conn, addr,runEvent):
    connectionOpen = True
    # sends a message to the client whose user object is conn
    #conn.send("Welcome to this chatroom!")
    lastRecv = time.perf_counter()
    buffer = b''
    while runEvent.is_set():
        if(time.perf_counter()-lastRecv > 10.0):
            print("client became unresponseive")
            break
        try:
            buffer += conn.recv(2048)
            while(len(buffer)>0):
                delimIndex = buffer.find(delim)

                #if delim in buffer:
                if(delimIndex!=-1):
                    frame = buffer[:delimIndex]
                    buffer = buffer[delimIndex+1:]
                    frame = ast.literal_eval(frame.decode("utf-8"))
                    lastRecv = time.perf_counter()
                    messageType = frame[FSNObjects.MESSAGE_TYPE_KEY]

                    # a player is senting an event
                    if messageType == FSNObjects.PLAYER_EVENT:
                        print("handling player event: "+str(frame))
                        connectionOpen = handlePlayerEvent(frame,conn)
                        if(connectionOpen == False):
                            break

                    #a player is sending an update about their current state
                    if messageType == FSNObjects.PLAYER_STATE:
                        sendAck(conn)
                        handlePlayerState(frame,conn)

        except Exception as e:
            print(traceback.format_exc())
            connectionOpen = False
            break
    try:
        conn.close()
    except:
        print(traceback.format_exc())
    try:
        remove(conn)
    except:
        print(traceback.format_exc())
    print("client thread ending")
def handlePlayerState(frame,conn):
    message = FSNObjects.PlayerState.getMessage(frame)

    senderID = message.senderID
    newClientState = frame
    with lock:
        clientStates[senderID] = newClientState
        clientConnections[senderID]['readyForData'] = True

def handlePlayerEvent(frame,conn):
    print("handlePlayerEvent")
    message = FSNObjects.PlayerEvent.getMessage(frame)
    broadcast(message,conn)
    #a new player is joining the game
    if(message.eventType==FSNObjects.PlayerEvent.PLAYER_JOINED):
        print("- player joined")
        #print("lock2 waiting...")
        with lock:
            #print("lock2 aquired")
            clientStates[message.senderID] = {}
            clientConnections[message.senderID] = {"socket":conn,"readyForData":True}
            #print("lock2 unlock")

        #let's tell the client what map we are on
        mapSetEvent = FSNObjects.ServerEvent(FSNObjects.ServerEvent.MAP_SET,mapContents)
        send(mapSetEvent,conn)

        #let's tell the client
        formatSetEvent = FSNObjects.ServerEvent(FSNObjects.ServerEvent.FORMAT_SET,formatContent)
        send(formatSetEvent,conn)

        #let's tell the client the state of the game
        serverState = FSNObjects.ServerState(clientStates,pickle.dumps(raceFormat))
        send(serverState,conn)

        #let's associate the player state with this socket
        #print("lock3 waiting...")
        with lock:
            #print("lock3")
            for key in clientStates:
                clientSocket = clientConnections[key]['socket']
                if(clientSocket == conn):
                    clientStates[key]['senderID'] = message.senderID
            #print("lock3 unlock")
        #let's let the new player know the state of the game
    #A player has just quit the game
    if(message.eventType==FSNObjects.PlayerEvent.PLAYER_QUIT):
        print("- player quit: "+str(message.senderID))
        connectionOpen = False
        return False

    #A player event has occured
    if(message.eventType==FSNObjects.PlayerEvent.PLAYER_MESSAGE):
        print("- player sent game message :"+str(message.extra))
        send(message, conn)

    #A player reset event has occured
    if(message.eventType==FSNObjects.PlayerEvent.PLAYER_RESET):
        print("- player sent game reset message :"+str(message.extra))
        send(message, conn)

    return True

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def sendAck(socket):
    ack = FSNObjects.ServerEvent(FSNObjects.ServerEvent.ACK)
    send(ack,socket)

def sendPlayerUpdates():
    with lock:
        tempStates = copy.deepcopy(clientStates)
    for senderID in tempStates:
        clientState = tempStates[senderID]
        if(clientState!={}): #this can be the case if the client just joined and we don't have a state yet
            if(len(str(clientState))<5):
                print("AHHHHHHH!!!!!!!! THERE WAS AN EMPTY CLIENT STATE THAT SLIPPED THROUGH!!!!")
            clientSocket = clientConnections[senderID]['socket']
            broadcast(clientState,clientSocket,highPriority=False)

def broadcast(message, socket, highPriority=True):
    with lock:
        senderIDs = clientConnections.keys()
    try:
        for senderID in senderIDs:
            with lock:
                clientSocket = clientConnections[senderID]['socket']
                clientReady = clientConnections[senderID]['readyForData']
            if clientSocket!=socket and (clientReady or highPriority):
                with lock:
                    clientConnections[senderID]['readyForData'] = False
                send(message,clientSocket)
    except Exception as e:
        print(traceback.format_exc())

def send(message, socket):
    try:
        dataOut = str(message).encode("utf-8")+delim
        with lock:
            socket.send(dataOut)
    except Exception as e:
        print(traceback.format_exc())
        socket.close()

def remove(socketToRemove):
    global clientStates
    global clientConnections
    connectionToDelete = None
    stateToDelete = None
    removedID = None

    with lock:
        for key in clientStates:
            clientSocket = clientConnections[key]['socket']
            if(clientSocket == socketToRemove):
                print("disconnecting client: "+str(key)+" on socket: "+str(socketToRemove))
                removedID = key

        if removedID!=None:
            del clientStates[removedID]
            del clientConnections[removedID]

        print("remaning clientStates: "+str(clientStates))
        print("remaning clientConnections: "+str(clientStates))

    print("notifying other clients of client removal")
    quitEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_QUIT,removedID)
    broadcast(quitEvent, None)

def main():
    global clientThreads
    global serverThread
    global clientThread
    global runEvent

    print("starting server thread")
    newServerThread = threading.Thread(target=serverThread,
        args=(None,None, runEvent)
    )
    newServerThread.start()

    while True:

        """Accepts a connection request and stores two parameters,
        conn which is a socket object for that user, and addr
        which contains the IP address of the client that just
        connected"""
        try:
            #print("waiting for new clients...")
            conn, addr = server.accept()
            conn.settimeout(10)
            """Maintains a list of clients for ease of broadcasting
            a message to all available people in the chatroom"""

            # prints the address of the user that just connected
            print(str(addr) + " connected")

            # creates and individual thread for every user
            # that connects
            #start_new_thread(clientThread,(conn,addr))
            newClientThread = threading.Thread(target=clientThread,
                args=(conn,addr,runEvent)
            )

            print("new client thread started")
            newClientThread.start()
            #print("lock6 waiting...")
            with lock:
                #print("lock6")
                clientThreads.append(newClientThread)
                #print("lock6 unlock")
            print("client thread started")
        except KeyboardInterrupt:
            server.close()
            print("Cleaning up threads...")
            runEvent.clear()
            for clientThread in clientThreads:
                print("cleaning thread "+str(clientThread))
                if(clientThread!=None):
                    clientThread.join()
            newServerThread.join()
            print("successfully joined client threads")

            break
        except:
            print(traceback.format_exc())
            break


if __name__=='__main__':
    main()


#WE NEED TO ONLY SEND CLIENT STATES TO CLIENTS WHO HAVE RECENTLY SENT US A MESSAGE (FOR CLIENTS WITH LOW FPS)
