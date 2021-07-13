'''
this is not doctype script - this is a comment that is long

make sure to add a userInterfaceHandler class and a userInterface class

UserInterfaceHandler => handles the information being sent and recieved from server

UserInterface => makes the information look asthetic for the user using the tkinter module python-3

'''

# imports
# socket is for communicating with server
import socket
# tkinter is the GUI components
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
# partial and functools is so that I can pass through parameters from tkinter functions
from functools import partial
# pickle is for pickling information into proper files
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
DISCONNECT_MESSAGE = b"!DISCONNECT"

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
        # self.name is formality
        self.name = 'userInterfaceHandler'
        # self.serveraddress is so that the uiHandler can locate and talk to the server
        self.serverAddress = ''
        # self.IMGpaths is a list of all the img paths so that there is a place to store all of the information
        self.IMGpaths = []

    def saveInformationLongTerm(self):
        # puts self.serverAddress variable into a temporary variable
        serverAddress = self.serverAddress

        # temporary variable gets saved into a serveraddress.dat file
        pickle.dump(serverAddress, open("serveraddress.dat", "wb"))

    def loadInformationLongTerm(self):
        # gets information from the serveraddress.dat file
        serverAddress = pickle.load(open("serveraddress.dat", "rb"))
        # loads the information from the serveraddress.dat file into the class __init__
        self.serverAddress = serverAddress

    def leaveConnection(self, userID):
        # this function logs out automatically and disconnects from the server safely
        # this signs out the user automatically and safely so that when the disconnect occurs, the user is not
        # shown as signed in by accident
        self.serverRequestUserSignOut(userID)
        # this disconnects the client from the server safely
        self.disconnect()

    def serverRequestLibraryName(self):
        # this function gets the name of the library so that the client can display it on the title of the window
        # for tkinter
        # this is the message for the function name call
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

    def serverRequestAddUser(self, name, email, password):
        # will be added later when home screen is finished and working
        pass

    def serverRequestUserSignIn(self, userID, password):
        # this asks the server to sign in the user with information.
        '''
        MAKE SURE THAT THE PASSWORD IS SENT SECURELY LATER ON IN THE CODE FOR PRODUCTION - IT IS CURRENTLY NOT ENCRYPTED
        AND IT IS ONLY BEING SEND THROUGH AS A PASSWORD AND THEN CONVERTED INTO HASH BY THE SERVER
        '''
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
        # this asks the server to sign out the user. password is not required to sign out user
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
        # this asks the server to delete a certain user
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
        # this asks the server to delete a certain book
        # once a book or a user has been deleted, it is not actually deleted
        # the status of the book or user is deleted, that way the information can still be retrieved and put back
        # into use
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
        # this asks the server for information on user
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
                return 'fail'

    def serverRequestRecommendedBooks(self):
        # this asks the server for information on books for recommended feed
        bookList = []
        imgPath = []
        # call function on server side
        message = b'showBooksForBrowse'
        msgLength = len(message)
        sendLength = str(msgLength).encode('utf-8')
        sendLength += b' ' * (HEADER - len(sendLength))
        client.send(sendLength)
        client.send(message)
        # get amount of books to retrieve
        msg = client.recv(HEADER).decode('utf-8')
        if msg:
            msg = int(msg)
            books = client.recv(msg).decode('utf-8')
            if books:
                books = int(books)
                for i in range(books):
                    msgLength = client.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        bookInformation = client.recv(msgLength)
                        bookInformation = pickle.loads(bookInformation)
                        bookList.append(bookInformation)
                    imgLength = client.recv(HEADER).decode('utf-8')
                    if imgLength:
                        imgLength = int(imgLength)
                        img = client.recv(imgLength)
                        f = open(f"temporaryFiles/test_file{i}.jpg", "wb")
                        f.write(img)
                        f.close()
                        imgPath.append(f"temporaryFiles/test_file{i}.jpg")

    def connect(self):
        # this connects to the server
        # try statement is to see if it can connect to the server using the serverAddress
        try:
            SERVER = self.serverAddress
            ADDR = (SERVER, PORT)
            client.connect(ADDR)
            return True
        except:
            # if it cannot connect to the server it sends the user to the server address page, where the user
            # can add their server address
            ui.serverAddressPage()

    def disconnect(self):
        # this is for safely disconnecting from the server
        # it sends a disconnect message and returns to regular code
        message = DISCONNECT_MESSAGE
        msgLength = len(message)
        sendLength = str(msgLength).encode('utf-8')
        sendLength += b' ' * (HEADER - len(sendLength))
        client.send(sendLength)
        client.send(message)

uiHandler = UserInterfaceHandler()


class UserInterface:
    def __init__(self):
        self.name = 'ui'
    
    def connect(self):
        x = uiHandler.connect()
        return x
    
    def userSettingsPage(self, username):
        def back():
            self.homePage(username)
    
        settingsPage = Tk()
    
    def homePage(self, username):
    
        def logoutandexit():
            if messagebox.askokcancel("ARE YOU SURE?", "ARE YOU SURE YOU WANT TO QUIT PROGRAM?"):
                uiHandler.serverRequestUserSignOut(username)
                uiHandler.disconnect()
                quit()
    
        logout = partial(logoutandexit)
    
        libraryName = uiHandler.serverRequestLibraryName()
        userInformation = uiHandler.serverRequestUserInformation(username)
    
        bookList = uiHandler.serverRequestRecommendedBooks()
    
        homeWindow = Tk()
        homeWindow.protocol("WM_DELETE_WINDOW", logoutandexit)
        homeWindow.geometry('700x525')
        homeWindow.title(f"{libraryName} User Home Page - {username}")
        homeWindow.resizable(False, False)
    
        settingsIMG = PhotoImage(file='Assets/settingsIcon.png')
        settingsIMG = settingsIMG.subsample(19, 19)
    
        logoutIMG = PhotoImage(file='Assets/logoutIcon.png')
        logoutIMG = logoutIMG.subsample(19, 19)
    
        browseIMG = PhotoImage(file='Assets/browseIcon.png')
        browseIMG = browseIMG.subsample(19, 19)
    
        homeIMG = PhotoImage(file='Assets/homeIcon.png')
        homeIMG = homeIMG.subsample(19, 19)
    
        message_frame = LabelFrame(homeWindow, padx=0, pady=0, width=700, height=108, bg='snow').grid(row=0, column=0)
        recommended_frame = LabelFrame(homeWindow, padx=0, pady=0, width=700, height=70, bg='DodgerBlue4').grid(row=1,
                                                                                                                column=0)
        line1_frame = LabelFrame(homeWindow, padx=0, pady=0, width=12, height=403, bg='steel blue').place(relx=0.72,
                                                                                                          rely=0.335)
        due_frame = LabelFrame(homeWindow, padx=0, pady=0, width=200, height=60, bg='steel blue').place(relx=0.735,
                                                                                                        rely=0.335)
        settingsbtn = ttk.Button(homeWindow, image=settingsIMG).place(relx=0.88, rely=0.01)
        logoutbtn = ttk.Button(homeWindow, image=logoutIMG, command=logout).place(relx=0.94, rely=0.01)
        browsebtn = ttk.Button(homeWindow, image=browseIMG).place(relx=0.82, rely=0.01)
        homebtn = ttk.Button(homeWindow, image=homeIMG).place(relx=0.76, rely=0.01)
    
        message = Label(message_frame, width=20, height=1, text=f"{userInformation['name'].upper()}",
                        font=('Courrier', 27, 'bold'), bg='snow', anchor='nw')
        message.place(relx=0.01, rely=0.03)
    
        recommended = Label(recommended_frame, width=40, text='RECOMMENDED BOOKS', font=('Courrier', 20, 'bold'), fg='snow',
                            bg='DodgerBlue4', anchor='w')
        recommended.grid(row=1, column=0)
    
        book_due = Label(due_frame, width=10, height=1, text="BOOKS DUE", font=('Courrier', 20, 'bold'), fg='snow',
                         bg='steel blue', anchor='w')
        book_due.place(relx=0.74, rely=0.355)
    
        homeWindow.mainloop()
    
    def loginPage(self):
        def closeProgram():
            uiHandler.disconnect()
            quit()
    
        def validateLogin(username, password):
            print("validating login...")
            confirm = uiHandler.serverRequestUserSignIn(username.get(), password.get())
            if confirm == 'True':
                print("USER SIGNED IN")
                tkWindow.destroy()
                self.homePage(username.get())
            else:
                messagebox.showinfo("ERROR", "INCORRECT USERID OR PASSWORD - please try again")
    
        def changeConnection():
            self.serverAddressPage()
    
        def registrationPage():
            tkWindow.destroy()
            self.registerPage()
    
        #window
        libraryName = uiHandler.serverRequestLibraryName()
    
        tkWindow = Tk()
        tkWindow.resizable(False, False)
        tkWindow.protocol("WM_DELETE_WINDOW", closeProgram)
        tkWindow.geometry('400x150')
        tkWindow.title(f"{libraryName} Login Page")
    
        #username label and text entry box
        usernameLabel = Label(tkWindow, text="UserID").grid(row=0, column=0)
        username = StringVar()
        usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)
    
        #password label and password entry box
        passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)
        password = StringVar()
        passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)
    
        validateLogin = partial(validateLogin, username, password)
    
        #login button
        loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)
    
        # make new account button
        registerButton = Button(tkWindow, text='make new account', command=registrationPage).place(relx=0.71, rely=0.8)
    
        # change server connection button
        serverConnectionButton = Button(tkWindow, text='change server connection', command=changeConnection).place(relx=0.63, rely=0.01)
    
        tkWindow.mainloop()
    
    def serverAddressPage(self):
        tkWindow = Tk()
        tkWindow.resizable(False, False)
        tkWindow.geometry('400x150')
        tkWindow.title("Change Server Address")
    
        def changeAddress(address):
            try:
                uiHandler.serverAddress = address.get()
                uiHandler.saveInformationLongTerm()
                self.connect()
                tkWindow.destroy()
                self.loginPage()
            except ValueError:
                print("UNABLE - SOMETHING WENT WRONG")
    
    
        serverAddressLabel = Label(tkWindow, text="Sever Address: ").grid(row=0, column=0)
        serverAddress = StringVar()
        serverAddressEntry = Entry(tkWindow, textvariable=serverAddress).grid(row=0, column=1)
    
        changeServerAddress = partial(changeAddress, serverAddress)
    
        loginButton = Button(tkWindow, text="Save Changes", command=changeServerAddress).grid(row=4, column=0)
    
        tkWindow.mainloop()
    
    def registerPage(self):
    
        def registerUser(name, email, password, password2):
            name = name.get()
            email = email.get()
            password = password.get()
            password2 = password2.get()
            if password != None and password2 != None and name != None and email != None:
                if password == password2:
                    uiHandler.serverRequestAddUser(name, email, password)
                else:
                    messagebox.showinfo("ERROR", "your password was not entered and re-entered correctly - please try again")
            else:
                messagebox.showinfo("ERROR", "you cannot leave textbox empty")
    
    
        homeWindow = Tk()
        homeWindow.geometry('400x200')
        homeWindow.title("TEST USER INTERFACE FOR HOME PAGE")
        homeWindow.resizable(False, False)
    
        main_frame = LabelFrame(homeWindow, padx=0, pady=0, width=200, height=50).grid(row=0, column=0)
        main_message = Label(main_frame, text="REGISTER NEW USER", font=('Courrier', 10, 'bold'), fg='black',
                             anchor='center')
        main_message.grid(row=0, column=0)
        second_frame = LabelFrame(homeWindow, padx=0, pady=0, width=200, height=50).grid(row=0, column=1)
        second_message = Label(main_frame, text="ENTER INFORMATION HERE", font=('Courrier', 10, 'bold'), fg='black',
                               anchor='center')
        second_message.grid(row=0, column=1)
        # name, email password
        nameLabel = Label(homeWindow, text="Enter Full Name:").grid(row=1, column=0)
        emailLabel = Label(homeWindow, text="Enter Email (this will be verified):").grid(row=2, column=0)
        passwordLabel = Label(homeWindow, text="Enter your Password:").grid(row=3, column=0)
        confirmpasswordLabel = Label(homeWindow, text="Re-Enter Your Password:").grid(row=4, column=0)
    
        fullnameEntry = Entry(homeWindow, textvariable='').grid(row=1, column=1)
        name = StringVar()
        e_mail__Entry = Entry(homeWindow, textvariable='').grid(row=2, column=1)
        email = StringVar()
        passwordEntry = Entry(homeWindow, textvariable='', show='*').grid(row=3, column=1)
        password = StringVar()
        passwrdEntry2 = Entry(homeWindow, textvariable='', show='*').grid(row=4, column=1)
        password2 = StringVar()
    
        register = partial(registerUser, name, email, password, password2)
    
        submit_button = Button(homeWindow, text='SUBMIT', command=register).place(relx=0.425, rely=0.8)
    
        homeWindow.mainloop()

ui = UserInterface()

try:
    uiHandler.loadInformationLongTerm()
except:
    ui.serverAddressPage()

try:
    x = ui.connect()
    if x == True:
        ui.loginPage()
except:
    pass

try:
    uiHandler.disconnect()
except:
    pass
