# All admin commands will now have to run through an admin account. This way only authorized personel can actually
# run admin commands through to the server. These include but are not limited to:
# delete user and/or delete book
# get information on user without user being signed in (obviously not including password)
# and close the server in general.
# once server has been closed, however. It will be impossible for the admin to open the server without starting up the
# code first.

'''
not doctype string

make sure to add the feature so that when books / users get deleted their data isn't on other books / users database
'''

# imports
# random import generates the IDs at random, so that you cannot use a malware program to predict a users ID number based
# off when why created the account.
# each ID is stored with information that the class of Library has access to.
import random
from datetime import date
from datetime import datetime
import pickle
import smtplib
import bcrypt
import socket
import threading



# constant variables
# protocol message header will be 64 bytes
HEADER = 64
# port 5050 is the connection port
PORT = 5050
# server IPV4 address
SERVER = socket.gethostbyname(socket.gethostname())
# server address binded by tuple
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

# this is information for the server socket import
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# this is contact information for the library messaging bot. the password is hidden when open sourced
serverEmail = 'librarysystem@gmail.com'
serverPassword = 'censored in github, only visible in source code as hash string'

# this here is admin information although proper admin code and authentication has not yet been added.
adminID = 3030
adminPassword = '1234'
adminEmail = 'prashunpoudyal26@gmail.com'

# this function is a thread and is responsible for handling the client
# in other words it sends and recieves data from and to the client(s)

def handleClient(conn, addr):
    '''
    this part of the code is responsible for handling the client.

    when information comes in from the client, it establishes what that means by a series of codes that is set
    by the server and the client in hard code. These codes contribute to certain functions.

    sometimes, the functions that are requested need to be given parameter so that the function can work. In this
    case, the server and the client both will understand that more information is coming, so the servers thread waits
    for a response. Once all the parameters have been satisfied, the function does its part.

    sometimes, the functions need to return information back to the user interface handler. To do this, the information
    will get returned the same way it came. With both parties understanding to wait for information to be recieved.

    This information cannot have a byte size of more than 99,999,999 bytes. The reason for this is that if it had larger
    bytes, the header code (which is 64 bytes long) cannot give a proper count. In the event that more than 100 MB of
    data must be sent, this will be reconfigured by me.

    currently data for book browsing is limited to 20 MB, about 1/5 of the possible. This is temporary and just because
    I do not want to test this as of now

    I will later put this into a class, called the serverHandler class
    '''
    library.globalPrint(f"[NEW CONNECTION] {addr} connected", 1, "systemLog")

    connected = True
    while connected:
        # this is a while loop to keep communication going.
        # this msgLength figures out how many bytes the next message will be. Maximum bytes as of now is
        # 99,999,999 bytes, or one byte under 100 MB. this can be changed later but for now this is what I have set it
        # to.
        msgLength = conn.recv(HEADER).decode('utf-8')
        if msgLength:
            # this is to check what the message actually is
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode('utf-8')
            # this is the information decoder - it translates the string code to a given function in
            # a given class
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print("A USER HAS DISCONNECTED")
                # this comment is so that pycharm will let me collapse the if statement
                # because if I want to collapse the if statement I need at least 2 lines
            # these are all the message codes.
            if msg == 'requestLibraryName':
                def requestLibraryName():
                    print("requestLibraryName")
                    name = library.name
                    name = name.encode('utf-8')
                    msgLength = len(name)
                    sendLength = str(msgLength).encode('utf-8')
                    sendLength += b' ' * (HEADER - len(sendLength))
                    conn.send(sendLength)
                    conn.send(name)
                requestLibraryName()
            if msg == 'requestSignIn':
                def clientRequestSignIn():
                    print("clientRequestSignIn")
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        userID = conn.recv(msgLength).decode('utf-8')
                        msgLength = conn.recv(HEADER).decode('utf-8')
                        if msgLength:
                            msgLength = int(msgLength)
                            password = conn.recv(msgLength).decode('utf-8')
                            signedIn = library.signInUser(userID, password)
                            # let UI know that sign in has been confirmed or rejected
                            confirm = str(signedIn).encode('utf-8')
                            msgLength = len(confirm)
                            sendLength = str(msgLength).encode('utf-8')
                            sendLength += b' ' * (HEADER - len(sendLength))
                            conn.send(sendLength)
                            conn.send(confirm)

                clientRequestSignIn()
            if msg == 'requestSignOut':
                def clientRequestSignOut():
                    print("clientRequestSignOut")
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        userID = conn.recv(msgLength).decode('utf-8')
                        library.signOutUser(userID)
                clientRequestSignOut()
            if msg == 'requestDeleteUser':
                def clientRequestDeleteUser():
                    print("clientRequestDeleteUser")
                    userID = None
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        userID = conn.recv(msgLength).decode('utf-8')
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        password = conn.recv(msgLength).decode('utf-8')
                        library.deleteUser(userID, password)
                clientRequestDeleteUser()
            if msg == 'requestUserInformation':
                def clientRequestUserInformation():
                    print("clientRequestUserInformation")
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        userID = conn.recv(msgLength).decode('utf-8')
                        userInformation = library.requestUserInformation(userID)
                        if userInformation['status'][2] == True:
                            print("sending information to client")
                            userInformation = pickle.dumps(userInformation)
                            msgRlength = len(userInformation)
                            sendRlength = str(msgRlength).encode('utf-8')
                            sendRlength += b' ' * (HEADER - len(sendRlength))
                            conn.send(sendRlength)
                            print(f"{sendRlength} \n {userInformation}")
                            conn.send(userInformation)
                            print("information sent on server side")
                        else:
                            print("incorrect login attmpt - not sending information to client")
                            msgR = 'None'
                            msgRlength = len(msgR.encode('utf-8'))
                            sendRlength = str(msgRlength).encode('utf-8')
                            sendRlength += b' ' * (HEADER - len(sendRlength))
                            conn.send(sendRlength)
                            conn.send(msgR.encode('utf-8'))
                clientRequestUserInformation()
            if msg == 'showBooksForBrowse':
                def clientShowBooksForBrowse():
                    print('clientShowBooksForBrowse')
                    # tell client the amount of books that will be sent
                    books = len(library.listBookClass)
                    books = str(books).encode('utf-8')
                    msgLength = len(books)
                    sendLength = str(msgLength).encode('utf-8')
                    sendLength += b' ' * (HEADER - len(sendLength))
                    conn.send(sendLength)
                    conn.send(books)

                    # retrieve information on book
                    for i in range(len(library.listBookClass)):
                        # send bookInformation
                        bookInformation = library.listBookClass[i].bookInformation
                        bookInformation = pickle.dumps(bookInformation)
                        msgLength = len(bookInformation)
                        sendLength = str(msgLength).encode('utf-8')
                        sendLength += b' ' * (HEADER - len(sendLength))
                        conn.send(sendLength)
                        conn.send(bookInformation)
                        # retrieve image path
                        imgPath = library.listBookClass[i].imgPath
                        f = open(imgPath, "rb")
                        img = f.read()
                        imgLength = len(img)
                        sendimgLength = str(imgLength).encode('utf-8')
                        sendimgLength += b' ' * (HEADER - len(sendimgLength))
                        conn.send(sendimgLength)
                        conn.send(img)
                        f.close()

                clientShowBooksForBrowse()

    library.saveInformationLongTerm()

def start():
    '''
    this function is also for handling clients, but it is only to wait for new clients to come in. It waits on the
    server.accept() function until someone joins the server. Once they have joined the rest of the code goes through,
    a new thread is made in the handleClient() function, and the start function rests back on the server.accept() to wait
    for a new user.

    when a user disconnects, it is set to false.
    '''
    running = True
    server.listen()
    library.globalPrint(f"SERVER IS LISTENING ON {SERVER}", 1, "systemLog")
    while running:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        library.globalPrint(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}", 1, "systemLog")

# library class acts as a server class
class Library:
    def __init__(self, name='new library'):
        '''
        all of the information in this __init__ class is stored into a .dat file so that the librarian does not
        have to re-enter all of the data in every time.
        '''
        # this constructor class will allow for the library to have certain pieces of information to be stored in itself
        self.name = name
        # these lists are for being able to count to see how many books and how many users there are
        # user ID is 5 digits, and book ID is 6 digits, so that it is easy to differ, and also because there
        # are generally more books than users in a library
        self.listUserID = []
        self.listBookID = []
        # these lists are the same thing, but instead are storing the exact class name rather than just the ID
        self.listUserClass = []
        self.listBookClass = []
        # these are message codes for emails

    def notifyAdmin(self):
        '''
        this function is for notifying admin when an incorrect login attempt has happened. This is a security function
        '''
        invalidLoginAttempt = f"Someone has attempted to login as administrator with an incorrect password at {datetime.now()}"
        self.notifyThroughEmail(adminEmail, invalidLoginAttempt)

    def notifyServerDue(self, bookInformation, status, userInformation=None):
        '''
        this function is used by the server to send emails to users about their book being due, overdue, or any
        other information they may need
        '''
        self.globalPrint(f"library.notifyServerDue(bookInformation, status) has been recieved. status = {status}", self.name, self.name)
        if status == 'due today':
            # find how long the list is
            historyLength = len(bookInformation['historyInformation'][2])
            userID = bookInformation['historyInformation'][2][historyLength]
            historyLength = len(bookInformation['historyInformation'][3])
            # retrieve user information
            userInformation = self.requestUserInformation(userID)
            self.notifyThroughEmail(userInformation['email'], f"To {userInformation['name']},\n\nThis email is sent from"
                                                              f" the {self.name} to let you know that you "
                                                              f"have the book {bookInformation['name']} due today. It is"
                                                              f"requested that you return this book to {self.name} by today"
                                                              f"or it will be flagged overdue.\n\n"
                                                              f"Yours Sincerely,\n\n"
                                                              f"{self.name}"
                                                              f"\n\n NOTE: THIS MESSAGE WAS SENT BY A BOT - DO NOT REPLY")
        if status == 'overdue':
            # find how long the list is
            historyLength = len(bookInformation['historyInformation'][2])
            userID = bookInformation['historyInformation'][2][historyLength]
            historyLength = len(bookInformation['historyInformation'][3])
            # retrieve user information
            userInformation = self.requestUserInformation(userID)
            self.notifyThroughEmail(userInformation['email'], f"To {userInformation['name']},\n\nThis email is sent from"
                                                              f" the {self.name} to let you know that you "
                                                              f"have the book {bookInformation['name']} now overdue. It is"
                                                              f"requested that you return this book to {self.name} immediately"
                                                              f"or it will be put on fee.\n\n"
                                                              f"Yours Sincerely,\n\n"
                                                              f"{self.name}"
                                                              f"\n\n NOTE: THIS MESSAGE WAS SENT BY A BOT - DO NOT REPLY")
        if status == 'confirmation of return':
            self.notifyThroughEmail(userInformation['email'], f"To {userInformation['name']},\n\nThis email is sent from"
                                                              f" the {self.name} to let you know that the book you took"
                                                              f"out, {bookInformation['name']} has been successfully returned.\n\n"
                                                              f"Yours Sincerely,\n\n"
                                                              f"{self.name}"
                                                              f"\n\n NOTE: THIS MESSAGE WAS SENT BY A BOT - DO NOT REPLY")

    def notifyThroughEmail(self, recievingEmail, message):
        '''
        server starts up, and it logs in to its own account. It will then send the email
        '''
        server = smtplib.SMTP('stmp.gmail.com', 587)
        server.starttls()
        server.login(serverEmail, serverPassword)
        self.globalPrint("EMAIL LOGIN SUCCESS", self.name, self.name)
        server.sendmail(serverEmail, recievingEmail, message)

    def loadInformationLongTerm(self):
        '''
        this function retrieves information that is stored on the hard drive
        '''
        try:
            self.listUserClass = pickle.load(open("serverData/saveUserClass.dat", "rb"))
        except Exception:
            self.globalPrint("ERROR: COULD NOT LOAD USER CLASS FILE", self.name, self.name)
        try:
            self.listBookClass = pickle.load(open("serverData/saveBookClass.dat", "rb"))
        except Exception:
            self.globalPrint("ERROR: COULD NOT LOAD USER LIST FILE", self.name, self.name)

        try:
            self.listUserID = pickle.load(open("serverData/saveUserID.dat", "rb"))
        except Exception:
            self.globalPrint("ERROR: COULD NOT LOAD BOOK CLASS FILE", self.name, self.name)

        try:
            self.listBookID = pickle.load(open("serverData/saveBookID.dat", "rb"))
        except Exception:
            self.globalPrint("ERROR: COULD NOT LOAD BOOK LIST FILE", self.name, self.name)

        print(f"{self.listUserClass}\n{self.listUserID}\n{self.listBookClass}\n{self.listBookID}")


    def saveInformationLongTerm(self):
        '''
        this function saves information that has been updated by the program
        '''

        userClass = self.listUserClass
        bookClass = self.listBookClass

        userID = self.listUserID
        bookID = self.listBookID

        self.globalPrint("Save Information Request Recieved", self.name, self.name)

        pickle.dump(userClass, open("serverData/saveUserClass.dat", "wb"))
        pickle.dump(bookClass, open("serverData/saveBookClass.dat", "wb"))
        pickle.dump(userID, open("serverData/saveUserID.dat", "wb"))
        pickle.dump(bookID, open("serverData/saveBookID.dat", "wb"))

        self.globalPrint("all Information has been saved to disk", self.name, self.name)

    def generateUserID(self):
        # this program is dealt with in the server so that a user is not able to choose his/her own ID, or so that one
        # can find the algorithm for generating the "random" IDs
        # it is important that the IDs are generated randomly for user security
        number = random.randint(10000, 99999)
        IDcount = self.listUserID.count(number)
        # this if and else statement make sure that the IDs are all unique and that there are no duplicates. that is
        # another reason why the server keeps a list of all of the user IDs
        if IDcount > 0:
            # this re-runs the function to generate a new number.
            self.generateUserID()
        else:
            # this part returns the number so that it is kept inside of the user class
            self.listUserID.append(number)
            return number

    def generateBookID(self):
        # this is the same code as for the generateUserID(self) function, but instead for book IDs notice the difference
        # in digits
        number = random.randint(100000, 999999)
        if self.listBookID.count(number) < 0:
            # this re-runs the function to generate a new number.
            self.generateBookID()
        else:
            self.listBookID.append(number)
            return number

    def addUser(self):
        # this adds the user and makes a class for the user given the parameters
        name = input("Full Name: ")
        email = input("Enter Email Address: ")
        password = input("Enter Password: ").encode('utf-8')
        confirmPassword = input("Re-Enter Password: ").encode('utf-8')
        if password == confirmPassword:
            user = User(name, email, bcrypt.hashpw(password, bcrypt.gensalt()))
            print(user.ID)
            print(user.password)
            self.listUserClass.append(user)

    def addBook(self):
        # this adds the book and makes a class for the book given the parameters. It takes more parameters than a user
        # because there is less required information for users
        name = input("Book Name: ")
        author = input("Authors Full Name: ")
        booknum = input("Book Number (if not a series, enter 1): ")
        category = []
        while True:
            # this while loop is so that you can add as many categories / keywords as you need until you no longer need it
            word = input("Enter a book Category (type exit when finished): ")
            if word == 'exit':
                break
            else:
                category.append(word)
        imgPath = input("Enter Image: ")

        book = Book(name, author, booknum, category, f"Assets/{imgPath}")
        self.listBookClass.append(book)
        print(book.ID)

    def requestUserInformation(self, userID):
        '''
        this retrieves user information in a neat way to make code look better.
        it is not really neccessary
        '''
        try:
            userID = int(userID)
        except ValueError:
            self.globalPrint("INVALID USER ID", self.name, self.name)
        doesExist = self.listUserID.count(userID)
        if doesExist > 0:
            for i in range(len(self.listUserClass)):
                if self.listUserClass[i].ID == userID:
                    return self.listUserClass[i].userInformation
            else:
                self.globalPrint("User ID Not Found", self.name, self.name)
                return None

    def requestBookInformation(self, bookID):
        # check if book exists, if book exists, then find information of the book, and return bookInformation
        doesExist = self.listBookID.count(bookID)
        if doesExist > 0:
            for i in range(len(self.listBookClass)):
                if self.listBookClass[i].ID == bookID:
                    return self.listBookClass[i].bookInformation
        else:
            self.globalPrint("Book Not Found", self.name, self.name)
            return 'Book Not Found'

    def showBooks(self, i):
        '''
        send book information of book depending on order of list. It is used for 'for' loops
        '''
        return self.listBookClass[i].bookInformation

    def userTakeoutBook(self, userInformation, bookInformation):
        '''
        here is how all of this works.
        the takeout book logic works as such:
        first the user class registers that a book has been taken out. It will then send a request information about the book.
        once that information is given to the user. The user (program not actual user) will confirm that it is the correct
        information, then it will contact the server with this function, to take out the book.

        Before any information is sent, all classes will do the user.updateInformation() and book.updateInformation() to
        make sure that the dictionaries are all up to date on their status. It will then finally be all sent to this program

        the two parameters are dictionaries of information, one of the user, one of the book. It will go through logic to
        make sure that both the book is available, and the user is qualified to take out the book.

        in order for it to work:
        1. user can't have overdue books
        2. book has to be available

        if user does have overdue books:
        user cannot take out book

        if book is not available:
        book can be placed on hold.

        if the book does get taken out, a timer will be added (later) to make sure that it knows when its overdue, and will
        send that information to the user through an email (which will be in a seperate file so that the email information
        and source code are not clogged with the same information, and also so that they can only talk one-way.
        '''
        # make sure book is available and that user has no overdue books
        if bookInformation['status'][0] == False or bookInformation['status'][1] == True:
            self.globalPrint(f"book available == {bookInformation['status'][0]}, book on hold == {bookInformation['status'][1]}", self.name, self.name)
            choice = input("book is not available. Would you like to put it on hold [Y/N]?")
            if choice.upper() == 'Y':
                self.putBookOnHold(userInformation, bookInformation)
        if bookInformation['status'][0] == True and bookInformation['status'][1] == False and userInformation['status'][0] == False:
            todaysDate = date.today()
            self.globalPrint("updating information...", self.name, self.name)
            # change book status to not available
            bookInformation['status'][0] = False
            # book information update history
            bookInformation['historyInformation'][0].append("Check Out")
            bookInformation['historyInformation'][1].append(todaysDate)
            bookInformation['historyInformation'][2].append(userInformation['identification'])
            bookInformation['historyInformation'][3].append(userInformation['name'])
            bookInformation['historyInformation'][4].append(todaysDate.replace(day=todaysDate.day+14))
            # user information update history
            userInformation['historyInformation'][0].append("Check Out")
            userInformation['historyInformation'][1].append(todaysDate)
            userInformation['historyInformation'][2].append(bookInformation['identification'])
            userInformation['historyInformation'][3].append(bookInformation['name'])
            userInformation['historyInformation'][4].append(todaysDate.replace(day=todaysDate.day+14))
            # change user status to 'check out books' = True
            userInformation['status'][3] = True
            userInformation['booksSignedOut'].append(bookInformation['identification'])
            # at this point all information is updated, now that information has to be sent out.
            self.updateInformation(userInformation, bookInformation)

    def globalPrint(self, information, name, ID):
        print(f"{name}-{ID}: {information}")

    def putBookOnHold(self, userInformation, bookInformation):
        # this is for putting book on hold by the user
        bookInformation['listOnHold'].append(userInformation['identification'])
        userInformation['status'][1] = True
        userInformation['listWaitingOnHold'].append(bookInformation['identification'])
        self.globalPrint("Book has been placed on hold, updating information now...", self.name, self.name)
        self.updateInformation(userInformation, bookInformation)

    def returnBook(self, userInformation, bookInformation):
        todaysDate = date.today()
        '''
        The idea here is that the information will come to here requesting a return. Once the book is returned. the
        status on the users side is now cancelled. The book will now be available IF there is no book on hold.
        '''
        # remove bookID from booksSignedOut for user
        userInformation['booksSignedOut'].remove(bookInformation['identification'])
        if len(userInformation['booksSignedOut']) == 0:
            # change user status for books signed out to 'False'
            userInformation['status'][3] = False
        else:
            pass

        try:
            # try to remove 'over due books'
            userInformation['listOverdueBooks'].remove(bookInformation['identification'])
        except:
            pass

        if len(userInformation['listOverdueBooks']) == 0:
            # turn off the status for overdue books
            userInformation['status'][0] = False
        else:
            pass

        if bookInformation['status'][1] == False:
            bookInformation['status'][0] = True
        else:
            self.shiftOnHold(bookInformation)

        bookInformation['historyInformation'][0].append("Check In")
        bookInformation['historyInformation'][1].append(todaysDate)
        bookInformation['historyInformation'][2].append(userInformation['identification'])
        bookInformation['historyInformation'][3].append(userInformation['name'])
        bookInformation['historyInformation'][4].append('None')

        userInformation['historyInformation'][0].append("Check In")
        userInformation['historyInformation'][1].append(todaysDate)
        userInformation['historyInformation'][2].append(bookInformation['identfication'])
        userInformation['historyInformation'][3].append(bookInformation['name'])
        userInformation['historyInformation'][4].append('None')

        self.updateInformation(userInformation, bookInformation)
        self.notifyServerDue(bookInformation, 'confirmation of return', userInformation)

    def shiftOnHold(self, bookInformation):
        # this shifts the next in line (on hold) to the new user
        # find the next user
        todaysDate = date.today()
        userID = bookInformation['listOnHold'][0]
        bookInformation['listOnHold'].remove(userID)
        if len(bookInformation['listOnHold']) == 0:
            bookInformation['status'][1] = False
        for i in range(len(self.listUserClass)):
            if self.listUserClass[i].ID == userID:
                userInformation = self.listUserClass[i].userInformation
                userInformation['listWaitingOnHold'].remove(bookInformation['identification'])
                if len(userInformation['listWaitingOnHold']) == 0:
                    userInformation['status'][1] = False
                userInformation['status'][3] = True
                userInformation['booksSignedOut'].append(bookInformation['identification'])
                userInformation['historyInformation'][0].append("Check Out")
                userInformation['historyInformation'][1].append(todaysDate)
                userInformation['historyInformation'][2].append(bookInformation['identification'])
                userInformation['historyInformation'][3].append(bookInformation['name'])
                self.updateInformation(userInformation, bookInformation)
                break
            else:
                continue

    def updateInformation(self, userInformation, bookInformation):
        # this updated the information of the user and / or the book
        self.globalPrint("sending information...", self.name, self.name)
        for i in range(len(self.listUserClass)):
            self.listUserClass[i].updateInformation(userInformation, userInformation['identification'])
        for i in range(len(self.listBookClass)):
            self.listBookClass[i].updateInformation(bookInformation, bookInformation['identification'])

    def signInUser(self, userID, password):
        '''
        this is the sign in function for the program

        it first makes sure all of the information needed is in the correct type, which is:
        str for password
        int for userID

        I later plan on making it so that you can log in with a username instead of a userID,
        but I will do that some other day when the UI is already finished.

        once it does that it makes sure that the UserID is valid, and if it is, the password
        associated with that userID is also valid.

        if they are all valid, then the user will allow authentication for information access.

        a feature will later be added to make sure you cannot pass in too much information at
        a time without it notifying both the user, the admin, and blocking you out from signing
        in for a period of time.
        '''
        try:
            userID = int(userID)
            password = password.encode('utf-8')
        except ValueError:
            self.globalPrint("userID must be a number", self.name, self.name)
            return False
        for i in range(len(self.listUserClass)):
            if self.listUserClass[i].ID == userID:
                if bcrypt.checkpw(password, self.listUserClass[i].password):
                    self.globalPrint(f"password correct for {userID}", self.name, self.name)
                    userInformation = self.listUserClass[i].userInformation
                    userInformation['status'][2] = True
                    print(userInformation)
                    self.listUserClass[i].updateInformation(userInformation, userID)
                    return True
                else:
                    self.globalPrint(f"password incorrect for {userID}", self.name, self.name)
                    return False
            else:
                pass

    def signOutUser(self, userID):
        try:
            userID = int(userID)
        except ValueError:
            self.globalPrint("userID must be a number", self.name, self.name)
        for i in range(len(self.listUserClass)):
            if self.listUserClass[i] == userID:
                userInformation = self.listUserClass[i].userInformation
                userInformation['status'][2] = False
                self.listUserClass[i].updateInformation(userInformation, userInformation['identification'])
                self.globalPrint(f"User {userID} has been registered as signed out", self.name, self.name)
            else:
                pass

    def deleteUser(self, ID, admPassword):
        try:
            ID = int(ID)
        except ValueError:
            self.globalPrint("YOUR USER ID IS INVALID", self.name, self.name)
        if admPassword == adminPassword:
            for i in range(len(self.listUserClass)):
                if self.listUserClass[i].ID == ID:
                    name = self.listUserClass[i].name
                    del self.listUserClass[i]
                    self.listUserID.remove(ID)
                    self.globalPrint(f"User {name}-{ID} has been successfully removed from the library", self.name, self.name)
                    break
                continue
        else:
            self.globalPrint("INCORRECT ADMIN PASSWORD", self.name, self.name)
            self.notifyAdmin()

    def deleteBook(self, ID, admPassword):
        try:
            ID = int(ID)
        except ValueError:
            self.globalPrint("YOUR BOOK ID IS INVALID", self.name, self.name)
        if admPassword == adminPassword:
            for i in range(len(self.listBookClass)):
                if self.listBookClass[i].ID == ID:
                    name = self.listBookClass[i].name
                    del self.listBookClass[i]
                    self.listBookID.remove(ID)
                    self.globalPrint(f"Book {name}-{ID} has been successfully removed from the library", self.name, self.name)
                    break
        else:
            self.globalPrint("INCORRECT ADMIN PASSWORD", self.name, self.name)
            self.notifyAdmin()

library = Library('test library')


# class for administrator

class Admin:
    def __init__(self, email, name, password):
        print("new admin added")
        self.email = email
        self.name = name
        self.password = password
        self.signIN = False

# class for User
class User:
    def __init__(self, name, email, password):
        print("new user added")
        # init function for user
        self.email = email
        self.name = name
        self.password = password
        self.signIn = False
        self.overdueBooks = False
        self.booksSignedOut = False
        self.listBooksSignedOut = []
        self.listOverdueBooks = []
        self.historyBook = []
        self.historyTime = []
        self.historyStatus = []
        self.historyBookName = []
        self.historyTimeReturn = []
        self.historyInformation = [self.historyStatus, self.historyTime, self.historyBook, self.historyBookName, self.historyTimeReturn]
        self.waitingOnHold = False
        self.listWaitingOnHold = []
        self.ID = library.generateUserID()
        self.status = [self.overdueBooks, self.waitingOnHold, self.signIn, self.booksSignedOut]
        # dictionary for information
        self.userInformation = {'email': self.email,
                                'name': self.name,
                                'status': self.status,
                                'historyInformation': self.historyInformation,
                                'listWaitingOnHold': self.listWaitingOnHold,
                                'booksSignedOut': self.listBooksSignedOut,
                                'identification': self.ID,
                                'listOverdueBooks': self.listOverdueBooks,
                                'signIn': self.signIn}

    def updateInformation(self, information, ID):
        if ID == self.ID:
            self.userInformation = information
            library.globalPrint('information has been updated successfully on user side', self.name, self.ID)
            print(self.userInformation)

    def requestBookInformation(self, bookID):
        # this is to ask the server for book information upon take out of the book.
        bookInformation = library.requestBookInformation(bookID)
        if bookInformation == 'Book Not Found':
            library.globalPrint("REQUEST FAILED", self.name, self.ID)
        else:
            return bookInformation

    def takeOutBook(self, bookInformation):
        # this is the function the class will use to contact the server for takeout of book
        # temporaryBookInformation = self.requestBookInformation()
        if self.signIn == True:
            library.userTakeoutBook(self.userInformation, bookInformation)


# class for Book
class Book:
    def __init__(self, name, author, booknum, category, imagePath):
        # init function for book
        print("new book has been created")
        self.name = name
        self.author = author
        self.booknum = booknum
        self.category = category
        self.available = True
        self.onHold = False
        self.imgPath = imagePath
        self.listOnHold = []
        self.historyStatus = []
        self.historyUser = []
        self.historyTime = []
        self.historyUserName = []
        self.historyTimeReturn = []
        self.ID = library.generateBookID()
        self.historyInformation = [self.historyStatus, self.historyTime, self.historyUser, self.historyUserName, self.historyTimeReturn]
        self.status = [self.available, self.onHold]
        self.bookInformation = {'name': self.name,
                                'author': self.author,
                                'booknum': self.booknum,
                                'status': self.status,
                                'listOnHold': self.listOnHold,
                                'historyInformation': self.historyInformation,
                                'historyTime': self.historyTime,
                                'identification': self.ID}

    def updateInformation(self, information, ID):
        # update information of the book in case something has changed
        if ID == self.ID:
            self.bookInformation = information
            library.globalPrint('information has successfully been updated on book side', self.name, self.ID)

    def listHistoryInformation(self):
        library.globalPrint(self.historyInformation, self.ID, self.name)

    def checkStatusForDate(self):
        timeReturn = len(self.historyTimeReturn)
        if date.today() == self.historyTimeReturn:
            library.globalPrint("THIS BOOK IS DUE", self.ID, self.name)
            library.notifyServerDue(self.bookInformation, 'due today')
        elif self.historyTimeReturn[timeReturn] < date.today():
            library.globalPrint(f"THIS BOOK IS OVERDUE BY {self.historyTimeReturn[timeReturn] - date.today()}", self.ID, self.name)
            library.notifyServerDue(self.bookInformation, 'overdue')

    def requestBookInformation(self):
        return self.bookInformation

try:
    library.loadInformationLongTerm()
    if library.listUserClass and library.listBookClass and library.listUserID and library.listBookID:
        library.globalPrint("files loaded on systemLog side", 1, "systemLog")
    else:
        library.globalPrint("could not load all files", 1, "systemLog")
except:
    library.globalPrint("files not found -- continuing anyways", 1, "systemLog")



library.globalPrint("SERVER IS STARTING...", 1, 'systemLog')

start()



# this code must be at end of file no matter what, it is server saving all information before program closes
library.saveInformationLongTerm()
