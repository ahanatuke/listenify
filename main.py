''' NOTE: this file will only run if init_db.py has been run
    at least once. otherwise, tables are never created.
    This must be fixed before handing in. '''

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
    return


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
    usersAmount = cursor.fetchone()
    connection.commit()

    usersAmount += 1
    print("Suggested user u", len(usersAmount), ": ")
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

    return



def main():

    #link database using URL 
    global path
    connection, cursor = connect(path)
    register()
    logReg = input("Would you like to login or register [L/R]? ")
    while logReg != "l" or logReg != "r":
        print("Incorrect input. Please try again.")
        logReg = input("Would you like to login or register [L/R]? ")
        print(logReg)
    if logReg == 'r':
        register()
    else: 
        login()
    connection.close()
main()