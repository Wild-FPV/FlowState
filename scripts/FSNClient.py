# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
import ast
import FSNObjects
import traceback
from uuid import getnode as get_mac

UPDATE_FRAMERATE = 30
MAX_SEND_BUFFER = 5

class FSNClient:
    def __init__(self, address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server.settimeout(10)
        self.serverIP = address#socket.gethostname()
        self.serverConnected = False
        self.serverPort = port#5069
        myIP = socket.gethostname()
        self.networkReady = False
        self.delim = b'\x1E'
        self.buffer = b''
        self.state = FSNObjects.PlayerState(None, None, None, None, None, None, None, None, None, None)
        self.messageHandler = None
        self.serverReady = True
        self.readyToQuit = False
        self.lastSentTime = time.time()
        self.clientID = str(time.perf_counter())+str(get_mac())
        self.ping = 0
        self.sendBufferCount = 0

    def connect(self):
        if(not self.serverConnected):
            self.server.connect((self.serverIP, self.serverPort))
            self.serverConnected = True
        else:
            print("server is already connected!")

    def recvFrame(self):
        frame = None
        read_sockets,write_socket, error_socket = select.select([self.server],[],[],0.0)
        for socks in read_sockets:
            try:
                self.buffer += socks.recv(4096)
                if(len(self.buffer)>4096):
                    print("WARNING: client can't keep up - "+str(len(self.buffer)))
                for i in range(0,1000):
                    if(len(self.buffer)>655360): #avoid getting spammed by large, bogus messages
                        print("WARNING: message too long! Disregarding")
                        self.buffer = b''
                        break
                    if(len(self.buffer)>0):
                        delimIndex = self.buffer.find(self.delim)
                        #if delim in buffer:
                        if(delimIndex!=-1):
                            frame = self.buffer[:delimIndex]
                            self.buffer = self.buffer[delimIndex+1:]
                            try:
                                frame = ast.literal_eval(frame.decode("utf-8"))
                                if(self.messageHandler!=None):
                                    if(frame!=None):
                                        self.messageHandler(frame)
                            except:
                                print("WARNING: got invalid frame! "+str(frame))
                                break

                        else:
                            break
                    else:
                        break

            except Exception as e:
                print(traceback.format_exc())
                print("WARNING: server unresponsive")
                self.quit()
                break
        return frame

    def updatePing(self):
        self.ping = (time.time()-self.lastSentTime)*1000

    def sendFrame(self,data):
        data+=self.delim
        self.server.send(data)

    def updateState(self,newState):
        self.state = newState

    def sendEvent(self,event):
        print("sending event: "+str(event))
        self.sendFrame(str(event).encode("utf-8"))

    def setMessageHandler(self,method):
        self.messageHandler = method

    def quit(self):
        print("quit")
        #quitEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_QUIT,self.clientID)
        #self.sendEvent(quitEvent)
        self.server.close()
        self.serverConnected = False

    def isConnected(self):
        return self.serverConnected

    def run(self):
        if(self.isConnected()): #the socket is still connected
            if(time.time()-self.lastSentTime>10.0):
                print("server unresponsive!")
            #if(self.serverReady and (time.time()-self.lastSentTime>1.0/UPDATE_FRAMERATE)) or (time.time()-self.lastSentTime>1):
            #if(self.serverReady and (time.time()-self.lastSentTime>1.0/UPDATE_FRAMERATE)) or ((self.sendBufferCount<10) and (time.time()-self.lastSentTime>1.0/UPDATE_FRAMERATE)):
            #the client will send at the desired frame rate, unless it hasn't seen a tick from the server in awhile
            #This ensures the server always has fresh data coming form the client
            if(self.sendBufferCount<MAX_SEND_BUFFER and time.time()-self.lastSentTime>1.0/UPDATE_FRAMERATE) or (time.time()-self.lastSentTime>1):
                #print("sending "+str(time.time()))
                self.lastSentTime = time.time()
                self.sendBufferCount += 1
                messageOut = str(self.state).encode("utf-8")
                self.sendFrame(messageOut)
                self.serverReady = False #this gets set true once we get another ack
            if self.sendBufferCount>=MAX_SEND_BUFFER:
                print("we are sending data too fast!!!")
                print(self.sendBufferCount)

            frame = self.recvFrame() #let's recv and handle anything the server has sent
