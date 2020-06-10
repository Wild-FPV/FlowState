import socket
import select
import sys
import pickle
import time
import ast

#dictionary keys
SENDER_ID_KEY = "SID"
MESSAGE_TYPE_KEY = "MT"
MESSAGE_DATA_KEY = "MD"
MESSAGE_EXTRA_KEY = "MX"

#server event keys
SERVER_EVENT_TYPE_KEY = "SET"
PLAYER_EVENT_TYPE_KEY = "PET"

DEFAULT_GAME_FORMAT = "tm"

#message types
SERVER_STATE = 1
SERVER_EVENT = 2
GAME_STATE = 10
GAME_EVENT = 11
PLAYER_STATE = 20
PLAYER_EVENT = 21


class Message:
    def __init__(self, senderID, messageType, extra=None):
        self.senderID = senderID
        self.messageType = messageType
        self.extra = extra

    @staticmethod
    def getMessage(message):
        Message.senderID = message[SENDER_ID_KEY]
        Message.messageType = message[MESSAGE_TYPE_KEY]
        Message.extra = message[MESSAGE_EXTRA_KEY]

    def __str__(self):
        message = {}
        message[SENDER_ID_KEY] = self.senderID
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)

class ServerEvent:
    #server event types
    PLAYER_JOINED = 0
    PLAYER_LEFT = 1
    SERVER_QUIT = 2
    ACK = 3
    MAP_SET = 4
    FORMAT_SET = 5

    def __init__(self, eventType, extra=None):
        self.messageType = SERVER_EVENT_TYPE_KEY
        self.eventType = eventType
        self.extra = extra

    #converts a dictionary object into a ServerEvent object
    @staticmethod
    def getMessage(message):
        obj = ServerEvent(message[SERVER_EVENT_TYPE_KEY], message[MESSAGE_EXTRA_KEY])
        return obj

    #converts this ServerEvent object into a string so that we can send it via tcp
    def __str__(self):
        message = {}
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[SERVER_EVENT_TYPE_KEY] = self.eventType
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)

class ServerState(Message):
    #player state keys
    PLAYER_STATES_KEY = "PS"
    GAME_MODE_KEY = "GM"
    def __init__(self, playerStates, gameMode=DEFAULT_GAME_FORMAT, extra=None):
        self.messageType = SERVER_STATE
        self.gameMode = gameMode
        self.playerStates = playerStates
        self.extra = extra

    @staticmethod
    def getMessage(message):
        obj = ServerState(message[ServerState.PLAYER_STATES_KEY],message[ServerState.GAME_MODE_KEY],message[MESSAGE_EXTRA_KEY])
        return obj

    def __str__(self):
        message = {}
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[ServerState.GAME_MODE_KEY] = self.gameMode
        message[ServerState.PLAYER_STATES_KEY] = self.playerStates
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)

class PlayerState(Message):
    #player state keys
    PLAYER_POSITION_KEY = "PP"
    PLAYER_ORIENTATION_KEY = "PO"
    PLAYER_COLOR_KEY = "PC"
    PLAYER_VTX_FREQUENCY_KEY = "PVF"
    PLAYER_VTX_POWER_KEY = "PVP"
    def __init__(self, senderID, extra, position, orientation, color, vtxFrequency, vtxPower):
        self.senderID = senderID
        self.messageType = PLAYER_STATE
        self.extra = extra
        self.position = position
        self.orientation = orientation
        self.color = color
        self.vtxFrequency = vtxFrequency
        self.vtxPower = vtxPower

    #this is where we deserialize a PlayerState object that we recieved from the server
    @staticmethod
    def getMessage(message):
        obj = PlayerState(message[SENDER_ID_KEY],message[MESSAGE_EXTRA_KEY],message[PlayerState.PLAYER_POSITION_KEY],message[PlayerState.PLAYER_ORIENTATION_KEY],message[PlayerState.PLAYER_COLOR_KEY], message[PlayerState.PLAYER_VTX_FREQUENCY_KEY], message[PlayerState.PLAYER_VTX_POWER_KEY])
        return obj

    #this is where we serialize the PlayerState object for sending across the wire
    def __str__(self):
        message = {}
        message[SENDER_ID_KEY] = self.senderID
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[MESSAGE_EXTRA_KEY] = self.extra
        message[self.PLAYER_POSITION_KEY] = self.position
        message[self.PLAYER_ORIENTATION_KEY] = self.orientation
        message[self.PLAYER_COLOR_KEY] = self.color
        message[self.PLAYER_VTX_FREQUENCY_KEY] = self.vtxFrequency
        message[self.PLAYER_VTX_POWER_KEY] = self.vtxPower
        return str(message)

class PlayerEvent:
    #player event types
    PLAYER_JOINED = 0
    PLAYER_QUIT = 1
    PLAYER_MESSAGE = 2
    PLAYER_RESET = 3

    #race event types
    EVENT_LAP = 4
    EVENT_RACE_FINISH = 5
    EVENT_HOLE_SHOT = 6
    EVENT_CHECKPOINT_COLLECT = 7

    def __init__(self, eventType, senderID, extra=None):
        self.messageType = PLAYER_EVENT
        self.eventType = eventType
        self.senderID = senderID
        self.extra = extra

    @staticmethod
    def getMessage(message):
        obj = PlayerEvent(message[PLAYER_EVENT_TYPE_KEY], message[SENDER_ID_KEY], message[MESSAGE_EXTRA_KEY])
        return obj

    def __str__(self):
        message = {}
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[SENDER_ID_KEY] = self.senderID
        message[PLAYER_EVENT_TYPE_KEY] = self.eventType
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)
