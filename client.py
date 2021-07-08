'''
this is not doctype script - this is a comment that is long

make sure to add a userInterfaceHandler class and a userInterface class

UserInterfaceHandler => handles the information being sent and recieved from server

UserInterface => makes the information look asthetic for the user using the tkinter module python-3

'''

# imports
import socket
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from functools import partial
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

'''
There are two classes in the client.py file.


first:
UserInterfaceHandler.

this class is used specifically for communicating with the UI, and with the server. It converts the information
from the server to the UI, or converts the information from the UI to give to the server.

essentially, it goes from computer readable information to user readable information, and is the midddleman
for the user side of communication.


second:
UserInterface

the UI class does not yet exist, but it is the class that displays information that looks good.

as of now it does not have anything other than log in and log out. Information about the UI design is available
on github as well.
'''
class UserInterfaceHandler:
    def __init__(self):
        self.name = 'userInterfaceHandler'

    def send(self, msg):
        message = msg.encode('utf-8')
        msgLength = len(message)
        sendLength = str(msgLength).encode('utf-8')
        sendLength += b' ' * (HEADER - len(sendLength))
        client.send(sendLength)
        client.send(message)

    def leaveConnection(self, userID):
        self.serverRequestUserSignOut(userID)
        self.disconnect()

    def serverRequestLibraryName(self):
        # message for function name
        message = b'requestLibraryName'
        msgLength = len(message)
        sendLength = str(msgLength).encode('utf-8')
        sendLength += b' ' * (HEADER - len(sendLength))
        client.send(sendLength)
        client.send(message)
        # message for user
        returnedmsgLength = client.recv(HEADER).decode('utf-8')
        if returnedmsgLength:
            returnedmsgLength = int(returnedmsgLength)
            message = client.recv(returnedmsgLength)
            message = message.decode('utf-8')
            return message

    def serverRequestUserSignIn(self, userID, password):
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
        # wait for return message
        returnedmsgLength = client.recv(HEADER).decode('utf-8')
        if returnedmsgLength:
            returnedmsgLength = int(returnedmsgLength)
            confirm = client.recv(returnedmsgLength).decode('utf-8')
            return confirm

    def serverRequestUserSignOut(self, userID):
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

    def adminRequestDeleteUser(self, userID, admPassword):
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

    def adminRequestDeleteBook(self, userID, admPassword):
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

    def serverRequestUserInformation(self, userID):
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
            try:
                returnedmsgLength = int(returnedmsgLength)
                userInformation = client.recv(returnedmsgLength)
                userInformation = pickle.loads(userInformation)
                return userInformation
            except:
                return None

    def serverRequestShowBooks(self):
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

    def connect(self):
        try:
            client.connect(ADDR)
        except ConnectionRefusedError:
            print("SERVER COULD NOT CONNECT TO CLIENT - EITHER YOU ARE AN INVALID CONNECTION OR THE SERVER IS DOWN")
        except ConnectionError:
            print("ConnectionError - something went wrong, please try again")
        except:
            print("Unknown Error - please try again")

        return True

    def main(self):
        print("main has started")

    def disconnect(self):
        self.send(DISCONNECT_MESSAGE)

uiHandler = UserInterfaceHandler()

uiHandler.connect()

def userSettingsPage(username):
    def back():
        homePage()

    settingsPage = Tk()


def homePage(username):
    def logoutandexit():
        if messagebox.askokcancel("ARE YOU SURE?", "ARE YOU SURE YOU WANT TO QUIT PROGRAM?"):
            uiHandler.serverRequestUserSignOut(username)
            uiHandler.disconnect()
            quit()

    libraryName = uiHandler.serverRequestLibraryName()
    homeWindow = Tk()
    homeWindow.geometry('600x450')
    userInformation = uiHandler.serverRequestUserInformation(username)
    print(userInformation)
    homeWindow.title(f"{libraryName} User Home Page - {username}")

    tabControl = ttk.Notebook(homeWindow)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='Home Page')
    tabControl.add(tab2, text='Browse Books')
    tabControl.add(tab3, text='Settings')
    tabControl.pack(expand=1, fill="both")

    ttk.Label(tab1, text=f"{userInformation['name']}").grid(row=0, column=0)
    btn = ttk.Button(tab1, text='Log Out & Exit', command=logoutandexit).grid(row=10, column=10)

    homeWindow.mainloop()


def loginPage():
    def validateLogin(username, password):
        print("validating login...")
        confirm = uiHandler.serverRequestUserSignIn(username.get(), password.get())
        if confirm == 'True':
            print("USER SIGNED IN")
            tkWindow.destroy()
            homePage(username.get())
        else:
            print(confirm)
            print("USER PASSWORD OR USERNAME IS INCORRECT")

    #window
    libraryName = uiHandler.serverRequestLibraryName()

    tkWindow = Tk()
    tkWindow.geometry('400x150')
    tkWindow.title(f"{libraryName} Login Page")

    #username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

    #password label and password entry box
    passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

    validateLogin = partial(validateLogin, username, password)

    #login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

    tkWindow.mainloop()

uiHandler.serverRequestUserSignOut('43103')

loginPage()

uiHandler.disconnect()
