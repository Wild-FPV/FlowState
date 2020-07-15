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
try:
    import winsound
except:
    pass

SOUND_PLAYER_CHECKPOINT = 0
SOUND_PLAYER_LEFT = 1
SOUND_PLAYER_JOIN = 2

raceband = [5658,5695,5732,5769,5806,5843,5880,5917]

def versionIs3():
    is3 = False
    if (sys.version_info > (3, 0)):
        is3 = True
    return is3

def getUserInput(prompt):
    if versionIs3():
        result = input(prompt)
    else:
        result = str(raw_input(prompt))
    return result

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.settimeout(10)
delim = b'\x1E'
IP_address = socket.gethostname()

port = getUserInput("Please input the port you'd like to use (or press return for default): ")
if(str(port)=="" or port==None):
    port = 50001
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
raceMetrics = {0:{"name":"First to complete race","format": RaceFormat.FORMAT_FIRST_TO_LAPS}, 1:{"name":"Most laps on race completion","format": RaceFormat.FORMAT_MOST_LAPS}, 2:{"name":"Fastest X consecutive laps","format": RaceFormat.FORMAT_FASTEST_CONSECUTIVE}}
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

def helpCommand():
    print("help - shows available server commands")
    print("states - print client states")
    print("connections - print client connections")
    print("timing - shows when each of the clients last responded")
    print("q - quits the server")

def statesCommand():
    print("states")
    with lock:
        print(clientStates)

def connectionsCommand():
    print("connections")
    with lock:
        print(clientConnections)

def recvTimesCommand():
    print("receive times")
    with lock:
        for clientID in clientConnections:
            connection = clientConnections[clientID]
            if('lastReady' in connection):
                timeDiff = time.time()-connection['lastReady']
            else:
                timeDiff = None
            print(str(clientID)+" last recv = "+str(timeDiff))

def quitCommand():
    print("server quitting")
    runEvent.clear()

#allows the server admin to debug the state of the server if something goes wrong
def debugThread(a,b,runEvent):
    lastSend = time.time()
    commands = {"help":helpCommand,"states":statesCommand,"connections":connectionsCommand,"timing":recvTimesCommand,"quit":quitCommand}
    while runEvent.is_set():
        command = getUserInput("Server running. Type \"help\" for help: ")
        try:
            commandCharacter = command
            commands[commandCharacter]()
        except Exception as e:
            print(e)
            print("invalid command \""+str(command)+"\"")

def playSound(sound):
    try:
        #
        #winsound.Beep(1046, 75)
        if(sound==SOUND_PLAYER_CHECKPOINT):
            winsound.PlaySound(r"C:\Users\Timothy\Documents\FlowState\sounds\checkpoint.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        if(sound==SOUND_PLAYER_JOIN):
            winsound.Beep(1046, 75)
        if(sound==SOUND_PLAYER_LEFT):
            winsound.Beep(1046, 75)
    except:
        pass

#handles compiling and sending the messages to each of the players
def serverThread(a,b,runEvent):
    lastSend = time.time()
    while runEvent.is_set():
        sendPlayerUpdates()
    print("client update thread ending...")

#handles receiving and parsing messages from each of the clients
def clientThread(conn, addr,runEvent):
    conn.settimeout(10)
    connectionOpen = True
    lastRecv = time.time()
    buffer = b''
    readyToAck = True
    while runEvent.is_set():
        if(connectionOpen):
            if(time.time()-lastRecv > 20.0): #time out the client if they become unresponsive
                print("client became unresponseive")
                break
            if(time.time()-lastRecv > 10.0):
                print("player hasn't sent a message in awhile...")
            try:
                buffer += conn.recv(2048)
                print(len(buffer))
                for i in range(0,100):
                    if(len(buffer)>65536): #avoid getting spammed by large, bogus messages
                        print("buffer overflowed!")
                        buffer = b''
                        break
                    if(len(buffer)>0):
                        if(not runEvent.is_set()):
                            break
                        delimIndex = buffer.find(delim)
                        #if delim in buffer:
                        if(delimIndex!=-1):
                            frame = buffer[:delimIndex]
                            buffer = buffer[delimIndex+1:]
                            frame = ast.literal_eval(frame.decode("utf-8"))
                            messageType = frame[FSNObjects.MESSAGE_TYPE_KEY]
                            lastRecv = time.time()
                            # a player is senting an event
                            if messageType == FSNObjects.PLAYER_EVENT:
                                try:
                                    if(frame[FSNObjects.PLAYER_EVENT_TYPE_KEY] == FSNObjects.PlayerEvent.EVENT_CHECKPOINT_COLLECT):
                                        playSound(SOUND_PLAYER_CHECKPOINT)
                                except Exception as e:
                                    print(e)
                                print("handling player event: "+str(frame))
                                connectionOpen = handlePlayerEvent(frame,conn)
                                if(connectionOpen == False):
                                    break

                            #a player is sending an update about their current state
                            if messageType == FSNObjects.PLAYER_STATE:
                                readyToAck = True
                                handlePlayerState(frame,conn)
                        else: #the buffer contains a partial message. Go recv more data
                            break
                    else: #we've read everything in the buffer
                        if(readyToAck): #one of the messages we processed was a player state update
                            readyToAck = False
                            sendAck(conn)
                        break

            except Exception as e:
                print(traceback.format_exc())
                connectionOpen = False
                break
        else:
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
    playSound(SOUND_PLAYER_LEFT)

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
    broadcast(message,conn,message.senderID)
    #a new player is joining the game
    if(message.eventType==FSNObjects.PlayerEvent.PLAYER_JOINED):
        playerName = message.extra['playerName']
        print(str(playerName)+" joined the race")
        playSound(SOUND_PLAYER_JOIN)
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

        teamRacing = False #in the future let's let the server admin set a team racing property. This should either allow or disallow video stomping
        if(teamRacing == False):
            #let's force the user to an open channel
            usedFrequencies = []
            with lock:
                for clientID in clientStates:
                    if(clientID!=message.senderID):
                        state = clientStates[clientID]
                        if(FSNObjects.PlayerState.PLAYER_VTX_FREQUENCY_KEY in state):
                            playerFrequency = state[FSNObjects.PlayerState.PLAYER_VTX_FREQUENCY_KEY]
                            usedFrequencies.append(playerFrequency)
            for channel in range(0,len(raceband)):
                frequency = raceband[channel]
                if(frequency not in usedFrequencies):
                    break

            serverEvent = FSNObjects.ServerEvent(FSNObjects.ServerEvent.SET_VTX_CHANNEL,channel)
            send(serverEvent,conn)

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
    ack = FSNObjects.ServerEvent(FSNObjects.ServerEvent.ACK,time.time())
    send(ack,socket)

def sendPlayerUpdates():
    with lock:
        for clientID in clientConnections:
            socket = clientConnections[clientID]['socket']
            clientReady = clientConnections[clientID]['readyForData']
            if clientReady:
                clientConnections[clientID]['readyForData'] = False
                sendAllClientStates(socket,clientID)
def sendAllClientStates(socket,senderID):
    with lock:
        for receiverID in clientStates:
            clientState = clientStates[receiverID]
            clientSocket = clientConnections[receiverID]['socket']
            if clientState!={}: #this can be the case if the client just joined and we don't have a state yet
                if receiverID!=senderID: #we don't need to send a clients state back to itself
                    send(clientState,socket)

def broadcast(message, socket, senderID, highPriority=True):
    try:
        with lock:
            for receiverID in clientConnections:
                clientSocket = clientConnections[receiverID]['socket']
                #clientReady = clientConnections[senderID]['readyForData']
                #if clientSocket!=socket and (clientReady or highPriority):
                #    clientConnections[senderID]['readyForData'] = False
                if(receiverID!=senderID):
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
        remove(socket)
        #socket.close()

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
    broadcast(quitEvent, None, None)

def main():
    global clientThreads
    global serverThread
    global debugThread
    global clientThread
    global runEvent

    print("starting server thread")
    newServerThread = threading.Thread(target=serverThread,
        args=(None,None,runEvent)
    )
    newServerThread.start()

    print("starting debug thread")
    newDebugThread = threading.Thread(target=debugThread,
        args=(None,None,runEvent)
    )
    newDebugThread.start()

    while runEvent.is_set():

        """Accepts a connection request and stores two parameters,
        conn which is a socket object for that user, and addr
        which contains the IP address of the client that just
        connected"""
        try:
            #print("waiting for new clients...")

            conn, addr = server.accept()
            conn.settimeout(20)
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
            newDebugThread.join()
            print("successfully joined client threads")

            break
        except socket.timeout:
            pass
        except:
            print(traceback.format_exc())
            break


if __name__=='__main__':
    main()


#WE NEED TO ONLY SEND CLIENT STATES TO CLIENTS WHO HAVE RECENTLY SENT US A MESSAGE (FOR CLIENTS WITH LOW FPS)
