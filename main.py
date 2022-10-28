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