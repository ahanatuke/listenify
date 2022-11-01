''' NOTE: this file will only run if init_db.py has been run
    at least once. otherwise, tables are never created.
    This must be fixed before handing in. '''

#todo add success checks to both login and register. should only continue if successful

import sqlite3
import getpass

path = './291_proj'


def connect(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor


#todo is this function ever used?  don't think it is. maybe destroy it
def introLoop():
    print("Press 'L' to login to an existing account.\nPress 'R' to register a new account.\nPress 'Q' to quit.")
    userInput = input("> ")
    userInput = userInput.lower().strip()
    while userInput != "r" and userInput != "l" and userInput != "q":
        print("Invalid input. Please try again.")
        userInput = input("> ")
        userInput = userInput.lower().strip()

    return userInput


def regInputs(suggestion, cursor):
    #todo TEST THIS BITCH
    validUid = False
    print("Suggested user ID: " + suggestion)
    while validUid == False:
        inputU = input("Please enter a user id (max 4 characters), or press enter to use the suggested: ")
        if inputU == "":
            inputU = suggestion
            validUid = True
        elif len(inputU) > 4:
            print("User ID is too long. ID can be at most 4 characters.")
        else:
            cursor.execute("""SELECT * FROM users WHERE uid = ?""", (inputU,))
            if cursor.fetchone() == None:
                validUid = True
            else:
                print("User ID is already taken.")

    inputN = input("Please enter your name: ")
    inputP = getpass.getpass(prompt="Enter a password: ")
    inputP2 = getpass.getpass(prompt="Re-enter password: ")
    while inputP != inputP2:
        print("Passwords don't match, please try again")
        inputP = getpass.getpass(prompt="Enter a password: ")
        inputP2 = getpass.getpass(prompt="Re-enter password: ")

    return inputU, inputN, inputP


def register():
    valid = True
    connection, cursor = connect(path)
    q = '''SELECT *
    FROM users
    '''
    cursor.execute(q)
    usersAmount = len(cursor.fetchall())
    connection.commit()

    #this functionality is probably unnecessary and yet, i did it anyway
    usersAmount += 1
    suggestion = "u"+str(usersAmount)
    cursor.execute('''SELECT * FROM users WHERE uid=?''', (suggestion,))
    while cursor.fetchone() != None:
        usersAmount += 1
        suggestion = "u" + str(usersAmount)
        cursor.execute('''SELECT * FROM users WHERE uid=?''', (suggestion,))

    inputU, inputN, inputP, inputP2 = regInputs(suggestion)

    reEnter = input("Keep the following [Y/N]?: \n" + inputU + "\n" + inputN + " \n (Press enter to cancel)")
    check = False

    while check == False:

        if reEnter.lower().strip() == 'n':
            inputU, inputN, inputP = regInputs()
            break
        elif reEnter.lower().strip() == 'y':
            q = '''INSERT INTO users 
            VALUES ((?), (?), (?))'''
            cursor.execute(q, (inputU, inputN, inputP))
            connection.commit()
            break
        elif reEnter == "":
            valid = False
            inputU = ""
            break
        else:
            print("Invalid input. Please try again")
            reEnter = input("Keep the following [Y/N]?: \n" + inputU + "\n" + inputN + " ")

    return valid, inputU


def login(cursor):
    #todo someone look at this and tell me if its okay lmao
    '''Login: nested loop unfortunately ready for this to run in O(n^2)?
            main loop to authenticate, then two loops inside that wait for valid info'''

    success = False
    valid = True
    uid = ""
    pwd = ""
    while ~success and valid:
        uidSuccess = False
        print("Please enter your User ID, or press enter to exit:")
        while ~uidSuccess and valid:
            uid = input("> ")
            if uid == "":
                valid = False
                break
            cursor.execute("SELECT * FROM USERS WHERE uid=?", (uid,))
            if cursor.fetchone() != None:
                uidSuccess = True
                break
            else:
                print("No user with that username. Please try again, or press enter to exit.")

        pwdSuccess = False
        print("Please enter the password for user %s, or press enter to change user" % uid)
        while ~pwdSuccess and valid:
            pwd = getpass.getpass("> ")
            if pwd == "":
                uidSuccess = False
                break
            cursor.execute("SELECT * FROM USERS WHERE uid=? AND pwd=?", (uid,pwd))
            if cursor.fetchone() != None:
                cursor.execute("SELECT name FROM USERS WHERE uid=? AND pwd=?", (uid,pwd))
                name = cursor.fetchone()
                print("Login Successful. Welcome " + name)
                return valid, uid
            else:
                print("Incorrect password. Please try again, or press enter to exit")

    return valid, uid




def main():
    print("291 Mini-Project 1\n")
    # todo please check i spelled your names right lmao
    print("By Anya Hanatuke, Alinn Martinez, and Ayaan Jutt\n")
    #todo link database using URL
    global path
    connection, cursor = connect(path)
    quitProgram = False
    while quitProgram == False:
        initialDone = False
        while initialDone == False and quitProgram == False:
            logReg = introLoop()
            if logReg == 'r':
                register()
                initialDone = True
            elif logReg == 'l':
                valid, uid = login(cursor)
                if valid == True:
                    initialDone = True
            elif logReg == 'q':
                quitProgram = True
                print("Thank you.")
                break

        sessionDone = False
        while ~sessionDone and ~quitProgram:
            #todo uh oh this is the hard part
            break


    connection.close()
main()