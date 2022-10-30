''' NOTE: this file will only run if init_db.py has been run
    at least once. otherwise, tables are never created.
    This must be fixed before handing in. '''

#todo add success checks to both login and register. should only continue if successful

from re import L
import sqlite3
import getpass
from tkinter import FALSE

path = './291_proj'


def connect(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor



def introLoop():
    print("Press 'L' to login to an existing account.\nPress 'R' to register a new account.\n")
    userInput = input("> ")
    userInput = userInput.lower().strip()
    while userInput != "r" and userInput != "l":
        print("Invalid input. Please try again.")
        userInput = input("> ")
        userInput = userInput.lower().strip()

    return userInput


def regInputs():
    inputU = input("Please enter a user id: ")
    inputN = input("Please enter your name: ")
    inputP = getpass.getpass(prompt="Enter a password: ")
    inputP2 = getpass.getpass(prompt="Re-enter password: ")
    while inputP != inputP2:
        print("Passwords don't match, please try again")
        inputP2 = getpass.getpass(prompt="Re-enter password: ")

    return inputU, inputN, inputP, inputP2


def register():
    connection, cursor = connect(path)
    q = '''SELECT *
    FROM users as u
    '''
    cursor.execute(q)
    usersAmount = len(cursor.fetchall())
    connection.commit()

    usersAmount += 1
    print("Suggested user u", usersAmount, ": ")
    inputU, inputN, inputP, inputP2 = regInputs()

    reEnter = input("Keep the following [Y/N]?: \n" + inputU + "\n" + inputN + " ")
    check = FALSE

    while check == FALSE:

        if reEnter.lower() == 'n':
            inputU, inputN, inputP, inputP2 = regInputs()
            break
        elif reEnter.lower() == 'y':
            q = '''INSERT INTO users 
            VALUES ((?), (?), (?))'''
            cursor.execute(q, (inputU, inputN, inputP))
            connection.commit()
            break
        else:
            print("Invalid input. Please try again")
            reEnter = input("Keep the following [Y/N]?: \n" + inputU + "\n" + inputN + " ")

    return inputU


def login(cursor):
    #todo someone look at this and tell me if its okay lmao
    '''Login: nested loop unfortunately ready for this to run in O(n^2)?
            main loop to authenticate, then two loops inside that wait for valid info'''

    success = False
    valid = True
    while ~success and valid:
        uidSuccess = False
        print("Please enter your User ID, or press enter to exit:")
        while ~uidSuccess and valid:
            uid = input("> ")
            if uid == "":
                valid = False
                break
            cursor.execute("SELECT * FROM USERS WHERE uid = ?", uid)
            if cursor.fetchone() is not None:
                uidSuccess = True
            else:
                print("No user with that username. Please try again, or press enter to exit.")


    return valid, uid


def main():
    print("291 Mini-Project 1\n")
    # todo please check i spelled your names right lmao
    print("By Anya Hanatuke, Alinn Martinez, and Ayaan Jutt\n")
    #todo link database using URL
    global path
    connection, cursor = connect(path)
    quit = False
    while ~quit:
        initialDone = False
        while ~initialDone:
            logReg = introLoop()
            if logReg == 'r':
                register()
                initialDone = True
            else:
                login(cursor)
                initialDone = True

        sessionDone = False
        while ~sessionDone:
            #todo uh oh this is the hard part
            break


    connection.close()
main()