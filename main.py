''' NOTE: this file will only run if init_db.py has been run
    at least once. otherwise, tables are never created.
    This must be fixed before handing in. '''

from re import L
import sqlite3
import getpass

path = './291_proj'


def connect(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor


def dropTables(cursor):
    drop_perform = "drop table if exists perform;"
    drop_artists = "drop table if exists artists;"
    drop_plinclude = "drop table if exists plinclude;"
    drop_playlists = "drop table if exists playlists;"
    drop_listen = "drop table if exists listen;"
    drop_sessions = "drop table if exists sessions;"
    drop_songs = "drop table if exists songs;"
    drop_users = "drop table if exists users;"

    cursor.execute(drop_perform)
    cursor.execute(drop_artists)
    cursor.execute(drop_plinclude)
    cursor.execute(drop_playlists)
    cursor.execute(drop_listen)
    cursor.execute(drop_sessions)
    cursor.execute(drop_songs)
    cursor.execute(drop_users)


def createTables(cursor):
    create_users = '''
                        create table users (
                            uid		char(4),
                            name		text,
                            pwd		text,
                            primary key (uid)
                        );'''

    create_songs = '''
                        create table songs (
                            sid		int,
                            title		text,
                            duration	int,
                            primary key (sid)
                        );'''

    create_sessions = '''
                        create table sessions (
                            uid		char(4),
                            sno		int,
                            start 	date,
                            end 		date,
                            primary key (uid,sno),
                            foreign key (uid) references users
                                    on delete cascade
                        );'''

    create_listen = '''
                        create table listen (
                            uid		char(4),
                            sno		int,
                            sid		int,
                            cnt		real,
                            primary key (uid,sno,sid),
                            foreign key (uid,sno) references sessions,
                            foreign key (sid) references songs
                        );'''

    create_playlists = '''
                        create table playlists (
                            pid		int,
                            title		text,
                            uid		char(4),
                            primary key (pid),
                            foreign key (uid) references users
                        );'''

    create_plinclude = '''
                        create table plinclude (
                            pid		int,
                            sid		int,
                            sorder	int,
                            primary key (pid,sid),
                            foreign key (pid) references playlists,
                            foreign key (sid) references songs
                        );'''

    create_artists = '''
                        create table artists (
                            aid		char(4),
                            name		text,
                            nationality	text,
                            pwd		text,
                            primary key (aid)
                        );'''

    create_perform = '''
                        create table perform (
                            aid		char(4),
                            sid		int,
                            primary key (aid,sid),
                            foreign key (aid) references artists,
                            foreign key (sid) references songs
                        );'''

    cursor.execute(create_users)
    cursor.execute(create_songs)
    cursor.execute(create_sessions)
    cursor.execute(create_listen)
    cursor.execute(create_playlists)
    cursor.execute(create_plinclude)
    cursor.execute(create_artists)
    cursor.execute(create_perform)



def register():
    connection, cursor = connect(path)
    q = '''SELECT *
    FROM users as u
    '''
    cursor.execute(q)
    usersAmount = cursor.fetchone()   
    connection.commit()

    
    usersAmount += 1
    print("Suggested user u" , len(usersAmount), ": ")
    inputU = input("Please enter a user id: ")
    inputN = input("Please enter your name: ")
    inputP = getpass.getpass(prompt = "Enter a password: ")
    return 


def login():
    return 
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