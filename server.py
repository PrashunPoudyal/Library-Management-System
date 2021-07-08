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
import sys

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

serverEmail = 'librarysystem@gmail.com'
serverPassword = 'librarySyst3mB0T'

adminID = 3030
adminPassword = '1234'
adminEmail = 'prashunpoudyal26@gmail.com'


def handleClient(conn, addr):
    library.globalPrint(f"[NEW CONNECTION] {addr} connected", 1, "systemLog")

    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode('utf-8')
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode('utf-8')
            # this is the information decoder - it translates the string code to a given function in
            # a given class
            if msg == DISCONNECT_MESSAGE:
                connected = False
                # this comment is so that pycharm will let me collapse the if statement
                # because if I want to collapse the if statement I need at least 2 lines
            if msg == 'requestSignIn':
                def clientRequestSignIn():
                    userID = None
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        userID = conn.recv(msgLength).decode('utf-8')
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        password = conn.recv(msgLength).decode('utf-8')
                        library.signInUser(userID, password)
                clientRequestSignIn()
            if msg == 'requestSignOut':
                def clientRequestSignOut():
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        userID = conn.recv(msgLength).decode('utf-8')
                        library.signOutUser(userID)
                clientRequestSignOut()
            if msg == 'requestDeleteUser':
                def clientRequestDeleteUser():
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
                    msgLength = conn.recv(HEADER).decode('utf-8')
                    if msgLength:
                        msgLength = int(msgLength)
                        userID = conn.recv(msgLength).decode('utf-8')
                        userInformation = library.requestUserInformation(userID)
                        userInformation = pickle.dumps(userInformation)
                        msgRlength = len(userInformation)
                        sendRlength = str(msgRlength).encode('utf-8')
                        sendRlength += b' ' * (HEADER - len(sendRlength))
                        conn.send(sendRlength)
                        conn.send(userInformation)
                        print("information sent on server side")
                clientRequestUserInformation()
            if msg == 'showBooksForBrowse':
                def clientShowBooksForBrowse():
                    bookInformationList = []

                    for i in range(len(library.listBookClass)):
                        bookInformationList.append(library.listBookClass[i].bookInformation)

                    # amount of information in the list
                    utfBookInformationList = pickle.dumps(bookInformationList)
                    msgLength = len(utfBookInformationList)
                    print(msgLength)
                    while msgLength > 20_000_000:
                        bookInformationList.pop()
                        utfBookInformationList = pickle.dumps(bookInformationList)
                        msgLength = len(utfBookInformationList)

                    sendLength = str(msgLength).encode('utf-8')
                    sendLength += b' ' * (HEADER - len(sendLength))
                    conn.send(sendLength)
                    conn.send(utfBookInformationList)



                clientShowBooksForBrowse()

    library.saveInformationLongTerm()


def start():
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
        invalidLoginAttempt = f"Someone has attempted to login as administrator with an incorrect password at {datetime.now()}"
        self.notifyThroughEmail(adminEmail, invalidLoginAttempt)

    def notifyServerDue(self, bookInformation, status, userInformation=None):
        self.globalPrint(f"library.notifyServerDue(bookInformation, status) has been recieved. status = {status}", self.name, self.name)
        if status == 'due today':
            # find how long the list is
            historyLength = len(bookInformation['historyInformation'][2])
            userID = bookInformation['historyInformation'][2][historyLength]
            historyLength = len(bookInformation['historyInformation'][3])
            userName = bookInformation['historyInformation'][2][historyLength]
            # retrieve user information
            userInformation = self.requestUserInformation(userID, userName)
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
            userName = bookInformation['historyInformation'][2][historyLength]
            # retrieve user information
            userInformation = self.requestUserInformation(userID, userName)
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
        server = smtplib.SMTP('stmp.gmail.com', 587)
        server.starttls()
        server.login(serverEmail, serverPassword)
        self.globalPrint("EMAIL LOGIN SUCCESS", self.name, self.name)
        server.sendmail(serverEmail, recievingEmail, message)

    def loadInformationLongTerm(self):
        self.listUserClass = pickle.load(open("saveUserClass.dat", "rb"))
        self.listBookClass = pickle.load(open("saveBookClass.dat", "rb"))
        self.listUserID = pickle.load(open("saveUserID.dat", "rb"))
        self.listBookID = pickle.load(open("saveBookID.dat", "rb"))
        print(f"\n{self.listUserClass}\n {self.listBookClass}\n {self.listUserID}\n {self.listBookID}")

    def saveInformationLongTerm(self):

        userClass = self.listUserClass
        bookClass = self.listBookClass

        userID = self.listUserID
        bookID = self.listBookID

        self.globalPrint("Save Information Request Recieved", self.name, self.name)

        pickle.dump(userClass, open("saveUserClass.dat", "wb"))
        pickle.dump(bookClass, open("saveBookClass.dat", "wb"))
        pickle.dump(userID, open("saveUserID.dat", "wb"))
        pickle.dump(bookID, open("saveBookID.dat", "wb"))

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

        book = Book(name, author, booknum, category)
        self.listBookClass.append(book)
        print(book.ID)

    def requestUserInformation(self, userID):
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
        self.globalPrint("sending information...", self.name, self.name)
        for i in range(len(self.listUserClass)):
            self.listUserClass[i].updateInformation(userInformation, userInformation['identification'])
        for i in range(len(self.listBookClass)):
            self.listBookClass[i].updateInformation(bookInformation, bookInformation['identification'])

    def signInUser(self, userID, password):
        try:
            userID = int(userID)
            password = password.encode('utf-8')
        except ValueError:
            self.globalPrint("userID must be a number", self.name, self.name)
        for i in range(len(self.listUserClass)):
            if self.listUserClass[i].ID == userID:
                if bcrypt.checkpw(password, self.listUserClass[i].password):
                    self.globalPrint(f"password correct for {userID}", self.name, self.name)
                    self.listUserClass[i].signIn = True
                else:
                    self.globalPrint(f"password incorrect for {userID}", self.name, self.name)
            else:
                pass

    def signOutUser(self, userID):
        try:
            userID = int(userID)
        except ValueError:
            self.globalPrint("userID must be a number", self.name, self.name)
        for i in range(len(self.listUserClass)):
            if self.listUserClass[i] == userID:
                self.listUserClass[i].signIn = False
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
                    self.globalPrint(f"User {name}-{ID} has been successfully removed from the library")
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
                                'listOverdueBooks': self.listOverdueBooks}

    def updateInformation(self, information, ID):
        if ID == self.ID:
            self.userInformation = information
            library.globalPrint('information has been updated successfully on user side', self.name, self.ID)

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
    def __init__(self, name, author, booknum, category):
        # init function for book
        print("new book has been created")
        self.name = name
        self.author = author
        self.booknum = booknum
        self.category = category
        self.available = True
        self.onHold = False
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

try:
    library.loadInformationLongTerm()
    library.globalPrint("files loaded on systemLog side", 1, "systemLog")
except:
    library.globalPrint("files not found -- continuing anyways", 1, "systemLog")


library.globalPrint("SERVER IS STARTING...", 1, 'systemLog')

start()


# this code must be at end of file no matter what, it is server saving all information before program closes
library.saveInformationLongTerm()
