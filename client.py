'''
this is not doctype script - this is a comment that is long

make sure to add a userInterfaceHandler class and a userInterface class

UserInterfaceHandler => handles the information being sent and recieved from server

UserInterface => makes the information look asthetic for the user using the tkinter module python-3

'''

# imports
import socket
import tkinter as tk
import pickle
'''
This file is the file that is on the user side. User Class will still be on library side. It is the userInterface that the
server is communicating with, and it is the server checking if the user class has proper authentication.

This is the client python file.

It is the part of the file that looks good.

socket is the import for client server

tkinter will be the userInterface GUI (similar to turtle graphics)
'''
# constant variables
# protocol message header will be 64 bytes
HEADER = 64
# port 5050 is the connection port
PORT = 5050
# disconnect message
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "26.229.251.28"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    message = msg.encode('utf-8')
    msgLength = len(message)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)

def serverRequestUserSignIn(userID, password):
    # message for function sign in
    message = b'requestSignIn'
    msgLength = len(message)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    # message for user
    userIDmessage = userID.encode('utf-8')
    msgLength = len(userIDmessage)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(userIDmessage)
    # message for password
    passwordMessage = password.encode('utf-8')
    msgLength = len(passwordMessage)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(passwordMessage)

def serverRequestUserSignOut(userID):
    # message for function sign in
    message = b'requestSignOut'
    msgLength = len(message)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    # message for user
    userIDmessage = userID.encode('utf-8')
    msgLength = len(userIDmessage)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(userIDmessage)

def adminRequestDeleteUser(userID, admPassword):
    # message for function sign in
    message = b'requestDeleteUser'
    msgLength = len(message)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    # message for user
    userIDmessage = userID.encode('utf-8')
    msgLength = len(userIDmessage)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(userIDmessage)
    # message for user
    password = admPassword.encode('utf-8')
    msgLength = len(password)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(password)

def adminRequestDeleteBook(userID, admPassword):
    # message for function sign in
    message = b'requestDeleteBook'
    msgLength = len(message)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    # message for user
    userIDmessage = userID.encode('utf-8')
    msgLength = len(userIDmessage)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(userIDmessage)
    # message for user
    password = admPassword.encode('utf-8')
    msgLength = len(password)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(password)

def serverRequestUserInformation(userID):
    # message for function sign in
    message = b'requestUserInformation'
    msgLength = len(message)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    # message for user
    userIDmessage = userID.encode('utf-8')
    msgLength = len(userIDmessage)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(userIDmessage)
    returnedmsgLength = client.recv(HEADER).decode('utf-8')
    if returnedmsgLength:
        returnedmsgLength = int(returnedmsgLength)
        userInformation = client.recv(returnedmsgLength)
        userInformation = pickle.loads(userInformation)
        return userInformation

def serverRequestShowBooks():
    message = b'showBooksForBrowse'
    msgLength = len(message)
    sendLength = str(msgLength).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    msgLength = client.recv(HEADER).decode('utf-8')
    if msgLength:
        msgLength = int(msgLength)
        booksList = client.recv(msgLength)
        booksList = pickle.loads(booksList)
        return booksList


def connect():
    try:
        client.connect(ADDR)
    except ConnectionRefusedError:
        print("SERVER COULD NOT CONNECT TO CLIENT - EITHER YOU ARE AN INVALID CONNECTION OR THE SERVER IS DOWN")
    except ConnectionError:
        print("ConnectionError - something went wrong, please try again")
    except:
        print("Unknown Error - please try again")

    return True

def main():
    print("main has started")
    send("HELLO THERE")

def disconnect():
    send(DISCONNECT_MESSAGE)

connect()

x = input('enter: ')

booksList = serverRequestShowBooks()

for i in range(len(booksList)):
    print(f"{booksList[i]}\n")

disconnect()
