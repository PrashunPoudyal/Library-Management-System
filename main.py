# sign in system has been introduced, though primitive. it is capable of saving information regarding the user and the
# book so that means that we can actually save information instead of having to rewrite it everytime.
# next we will add logic for adding to hold list, count down until it is overdue, as well as contacting user and admin
# through email address

# imports
# random import generates the IDs at random, so that you cannot use a malware program to predict a users ID number based
# off when why created the account.
# each ID is stored with information that the class of Library has access to.
import random
from datetime import date
# import tkinter as tk


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

    def loadInformationLongTerm(self):
        self.globalPrint("load information request recieved", self.name, self.name)
        loadFile = open("saveUserClass.txt", "r")
        self.listUserClass = loadFile.read()
        loadFile.close()
        self.globalPrint("loaded user class list", self.name, self.name)
        loadFile = open("saveBookClass.txt", "r")
        self.listBookClass = loadFile.read()
        loadFile.close()
        self.globalPrint("loaded book class list", self.name, self.name)
        loadFile = open("saveUserID.txt", "r")
        self.listUserID = loadFile.read()
        loadFile.close()
        self.globalPrint("loaded user ID list", self.name, self.name)
        loadFile = open("saveBookID.txt", "r")
        self.listBookID = loadFile.read()
        loadFile.close()
        self.globalPrint("loaded book ID list", self.name, self.name)


    def saveInformationLongTerm(self):
        userClass = self.listUserClass
        bookClass = self.listBookClass

        userID = self.listUserID
        bookID = self.listBookID

        saveFile = open("saveUserClass.txt", "w")
        saveFile.write(str(userClass))
        saveFile.close()

        saveFile = open("saveBookClass.txt", "w")
        saveFile.write(str(bookClass))
        saveFile.close()

        saveFile = open("saveUserID.txt", "w")
        saveFile.write(str(userID))
        saveFile.close()

        saveFile = open("saveBookID.txt", "w")
        saveFile.write(str(bookID))
        saveFile.close()

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
        IDcount = self.listBookID.count(number)
        if IDcount > 0:
            # this re-runs the function to generate a new number.
            self.generateBookID()
        else:
            self.listBookID.append(number)
            return number

    def addUser(self):
        # this adds the user and makes a class for the user given the parameters
        name = input("Full Name: ")
        email = input("Enter Email Address: ")
        password = input("Enter Password: ")
        confirmPassword = input("Re-Enter Password: ")
        if password == confirmPassword:
            user = User(name, email, password)
            print(user.ID)
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

    def requestUserInformation(self, userID, userName):
        doesExist = self.listUserID.count(userID)
        if doesExist > 0:
            for i in range(len(self.listUserClass)):
                if self.listUserClass[i].ID == userID and self.listUserClass[i].name == userName and self.listUserClass[i].signIn:
                    return self.listUserClass[i].userInformation
                if self.listUserClass[i].ID == userID and self.listUserClass[i].name == userName and not self.listUserClass[i].signIn:
                    self.globalPrint("USER NOT PROPERLY SIGNED IN - library.requestUserInformation cannot return information", self.name, self.name)
                    return None
            else:
                self.globalPrint("User ID Not Found", self.name, self.name)

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
        if bookInformation['status'][0] == True and bookInformation['status'][1] == False and userInformation['status'][0] == False:
            self.globalPrint("updating information...", self.name, self.name)
            bookInformation['status'][0] = False
            bookInformation['history'].append(userInformation['identification'])
            userInformation['history'].append(bookInformation['identification'])
            todaysDate = date.today()
            bookInformation['historyTime'].append(todaysDate)
            userInformation['historyTime'].append(todaysDate)
            userInformation['status'][3] = True
            userInformation['booksSignedOut'].append(bookInformation['identification'])
            # at this point all information is updated, now that information has to be sent out.
            self.updateInformation(userInformation, bookInformation)

    def globalPrint(self, information, name, ID):
        print(f"{name}-{ID}: {information}")

    def putBookOnHold(self, userInformation, bookInformation):
        pass
        # when the book is placed on hold this is the final stage

    def updateInformation(self, userInformation, bookInformation):
        self.globalPrint("sending information...", self.name, self.name)
        for i in range(len(self.listUserClass)):
            self.listUserClass[i].updateInformation(userInformation, userInformation['identification'])
        for i in range(len(self.listBookClass)):
            self.listBookClass[i].updateInformation(bookInformation, bookInformation['identification'])

    def signInUser(self, ID, password):
        for i in range(len(self.listUserClass)):
            if self.listUserClass[i].ID == ID:
                break
            else:
                continue
        for i in range(len(self.listUserClass)):
            status = self.listUserClass[i].requestSignIn(password)
            if status == True:
                self.globalPrint('SIGN IN CONFIRMED ON SERVER SIDE', self.name, self.name)
                signInformation = [ID, self.listUserClass[i].name]
                return signInformation
            else:
                print("YOU HAVE ENTERED AN INCORRECT PASSWORD")
                break

    def signInInput(self):
        IDnumber = input("Enter ID: ")
        try:
            IDnumber = int(IDnumber)
        except:
            pass

        validateID = self.listUserID.count(IDnumber)
        if validateID > 0:
            password = input("Please Enter Password: ")
            signInformation = self.signInUser(IDnumber, password)
            return signInformation

    def deleteUser(self, ID):
        for i in range(len(self.listUserClass)):
            if self.listUserClass[i].ID == ID:
                del self.listUserClass[i]
                self.listUserID.remove(ID)
                print("USER HAS BEEN SUCCESSFULLY DELETED YOU WILL NOW RETURN TO MAIN SCREEN")
                break
            continue

    def deleteBook(self, ID):
        for i in range(len(self.listBookClass)):
            if self.listBookClass[i].ID == ID:
                del self.listBookClass[i]
                self.listBookID.remove(ID)
                print("BOOK HAS BEEN SUCCESSFULLY DELETED YOU WILL NOW RETURN TO MAIN SCREEN")
                break


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
        self.history = []
        self.historyTime = []
        self.waitingOnHold = False
        self.listWaitingOnHold = []
        self.ID = library.generateUserID()
        self.status = [self.overdueBooks, self.waitingOnHold, self.signIn, self.booksSignedOut]
        # dictionary for information
        self.userInformation = {'email': self.email,
                                'name': self.name,
                                'status': self.status,
                                'history': self.history,
                                'historyTime': self.historyTime,
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

    def requestSignIn(self, password):
        if password == self.password:
            self.signIn = True
            library.globalPrint("sign in confirmed on user side", self.name, self.ID)
            return True


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
        self.history = []
        self.historyTime = []
        self.ID = library.generateBookID()
        self.status = [self.available, self.onHold]
        self.bookInformation = {'name': self.name,
                                'author': self.author,
                                'booknum': self.booknum,
                                'status': self.status,
                                'history': self.history,
                                'historyTime': self.historyTime,
                                'identification': self.ID}

    def updateInformation(self, information, ID):
        # update information of the book in case something has changed
        if ID == self.ID:
            self.bookInformation = information
            library.globalPrint('information has successfully been updated on book side', self.name, self.ID)


try:
    library.loadInformationLongTerm()
    library.globalPrint("files loaded on systemLog side", 1, "systemLog")
except:
    library.globalPrint("files not found -- continuing anyways", 1, "systemLog")


# this code must be at end of file no matter what, it is server saving all information before program closes
library.saveInformationLongTerm()
