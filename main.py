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


def regInputs():
    inputU = input("Please enter a user id: ")
    inputN = input("Please enter your name: ")
    inputP = getpass.getpass(prompt = "Enter a password: ")
    inputP2 =  getpass.getpass(prompt = "Re-enter password: ")
    while inputP != inputP2: 
        print("Passwords don't match, please try again")
        inputP2 =  getpass.getpass(prompt = "Re-enter password: ")
    
    return inputU, inputN, inputP, inputP2

def register():
    connection, cursor = connect(path)
    q = '''SELECT *
    FROM users as u
    '''
    cursor.execute(q)
    usersAmount = len(cursor.fetchall()) + 1   
    connection.commit()

    print("Suggested user u" , usersAmount, ": ")
    inputU, inputN, inputP, inputP2 = regInputs()
   
    reEnter = input("Keep the following [Y/N]?: \n"+inputU+"\n"+inputN+" ")
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
            reEnter = input("Keep the following [Y/N]?: \n"+inputU+"\n"+inputN+" ")

    return  

 


def login(cursor):
    #todo someone look at this and tell me if its okay lmao
   
    return



def introLoop():
    print("Press 'L' to login to an existing account.\nPress 'R' to register a new account.\nPress 'Q' to quit.")
    userInput = input("> ")
    userInput = userInput.lower().strip()
    while userInput != "r" and userInput != "l" and userInput != "q":
        print("Invalid input. Please try again.")
        userInput = input("> ")
        userInput = userInput.lower().strip()
    return userInput

def addSong():
    '''CONCEPT: ask for title and duration as inputs
    get all songs and create a new sid by adding length of all songs + 1
    from there see if we can select a song from the input provided by the artist 
    a song provided by the artist should be unique, and therefore if we check the len of songExist we should get a len of 0
    If the song doesn't exist we insert it, and then request an input about who the features are, once provided do a for loop and add every feature
    Make sure to confirm that is either added in or exists
    
    TO DO: check if it works'''
    
    connection, cursor = connect(path)
   
   #get all songs and get len 
    q = '''SELECT *
            FROM songs as s'''
    cursor.execute(q)
    sidNew = len(cursor.fetchall()) + 1
    connection.commit()

    print("Please enter the title and duration (in seconds): ")
    title = input("Title: ")
    duration = input("Duration (in seconds): ")
    duration = int(duration)
    
    #CHECK IF THE SONG EXISTS
    q = '''SELECT  s.title, s.duration
        FROM songs as s, artists as a, perform as p
        WHERE s.title = ? AND s.duration = ? AND a.aid = ? AND p.sid = s.sid AND p.aid = a.aid 
        '''
    cursor.execute(q, (title, duration, artist, ))
    #1 song should exist like this, len of fetchone = 0 it should be unique HYPOTHETICALLY
    songExist = len(cursor.fetchone())
    connection.commit()

    if songExist == 0: 
        q = '''INSERT INTO songs 
        VALUES(?, ?, ?)'''
        cursor.execute(q, (sidNew, title, duration,))
        connection.commit()
        userInput = input("Please list the aid's of everyone who is featured on your song (hit ENTER if none): ")
        inputChecker = userInput.split()
        if inputChecker != '':
            result = [x.strip() for x in userInput.split(',')]
            #assuming we dont need to validate aids for every feature 
            for feature in result:
                q = '''INSERT INTO perform 
                VALUES (?, ?)'''
                cursor.execute(q, (feature, sidNew))
                connection.commit()
        print("Song %s has been successfully added in." %songExist)
            
        
    else:
        print("Cannot add, this song already exists.")
        
    return

def topListen():
    ''' TO DO: 
    see if these actually work and finish the FROMS and WHERES'''
    
    
    connection, cursor = connect(path)
    q = '''SELECT u.uid
    FROM
    WHERE
    ORDER BY u.uid DESC
    LIMIT 3
    '''
    cursor.execute(q)
    top3U = cursor.fetchall()
    connection.commit()
    for user in top3U:
        print(user)

    
    q = '''SELECT p.pid
    FROM
    WHERE
    ORDER BY p.pid DESC
    LIMIT 3
    '''
    cursor.execute(q)
    top3P = cursor.fetchall()
    connection.commit()
    for playlist in top3P:
        print(playlist)

def artist(artist):
    '''TO DO: check if it works, 
    add a way to logout'''
    #artist is an aid of the user who logged in, used to check if a song exists or not 
    connection, cursor = connect(path)
    print("Enter 'S' to add a song.\nEnter 'F' to find your top listeners and playlists with most of your songs.")
    userInput = input("> ")
    userInput = userInput.lower().strip()
    while userInput != "s" and userInput != "f":
        if userInput == 's': 
                addSong()
        elif userInput == 'f':
            topListen()
        else:
            print("Invalid input. Please try again.")
            userInput = input("> ")
            userInput = userInput.lower().strip()
    return 



def startSess():
    '''TO DO: Check if it works'''
    
    connection, cursor = connect(path)
    
    #get all sessions and add 1 to get a next sno
    q = '''SELECT *
        FROM sessions'''
    cursor.execute(q)
    newSession = len(cursor.fetchall()) + 1
    connection.commit()
    
    #add the session in
    q = '''
    INSERT INTO sessions(sno, start, end)
    VALUES(?, datetime('now'), NULL)
    '''
    cursor.execute(q, (newSession,))
    connection.commit()

    return newSession 

def endSess(sessNo):
    '''TO DO: Check if it works'''
    
    connection, cursor = connect(path)
    q = '''INSERT INTO sessions(end)
    VALUES(datetime('now'))
    WHERE sessions.sno = ?'''
    cursor.execute(q, (sessNo))
    connection.commit()

    return 
    
def orderByKW(arr, keys):
    '''TO DO: order the tuples so that the one with the most matched keywords is at the top of the list
    RETURN THE LIST '''
    #arr is the tuple, keys is the keyword, order DESC with the top
    #most array being the one with the most key words matched
    return


def songInfo():
    ''' Finish the query '''
    
    #get artist name, sid, title and duration + any playlist the song is in
    connection, cursor = connect(path)
    q = '''SELECT
    FROM
    WHERE'''
    cursor.execute(q)
    songInfo = cursor.fetchone()
    connection.commit()

    for info in songInfo: 
        print(info)

    return

def user(user):
    '''LOTS TO DO:
    ***___*** => things to start on 
    
    '''
    #user is an uid of the user to logged in
    connection, cursor = connect(path)


    print("To start a session enter 'S'\n To search for a song or playlist enter 'K'\nEnter 'A' to search for an artist\nTo end the session press 'E': ")
    userInput = input("> ")
    userInput = userInput.lower().strip()
    
    if userInput == 's':
        sessNo = startSess()
    elif userInput == 'k':
        #" user should be able to provide one or more unique keywords,"
        # FOCUS ON: Either having it be one input split into an array or requesting multiple inputs for keywords (probably the best????)
        #must indicate if playlist or song is displayed

        userInput = input("Please enter keywords to search for playlists or songs by spaces only.\n>")
        
        #get the keywords into an array
        keyWords = userInput.split()
        
        '''*** TO DO: get the rows, even if they're unordered thats okay we'll sort it in orderbyKW() *** '''
        #get all matching rows from keywords
        q = ''' 

        SELECT 
        FROM 
        WHERE

        '''
        cursor.execute(q)
        allMatching = cursor.fetchall()
        connection.commit()

      
        '''TO DO: 
        ***FIRST: order the tuples by what has the most keywords
        SECOND: print the 5 out
        THIRD: ask what the user wants to do
        
        ***
        '''
        orderedList = orderByKW(allMatching, keyWords)
        
        #print the first 5
        index = 0
        while index < 5:
            print(allMatching[index])
            index += 1 
        
        ''' *** TO DO: find a way to distinguish btwn playlist and song and how to enter a specific one*** 
        one thing to note is that neither song or playlist has a letter to distinguish itself as an id
                i.e. sid of wavin flag would be 1 and not s1
        ways to solve this: maybe look into finding a way within the for loop to attach an s or a p to the id?
        only playlists have users, and only song have duration, look into that or other ways to distinguish whats a playlist. 
       '''
        print("Enter the id of a playlist or song you want to select as (playlist/song [number])\nEnter 'N' to go to the next 5\Hit 'ENTER' to leave")
        userInput = input("> ")
        userInput = userInput.lower().strip()
        
        while(userInput[0] != ''):
            #leave
            if userInput[0] == '':
                return
            
            #focus on getting song1 to see what the user inputs is a song or a playlist
            elif userInput[0] == 'song' and int(userInput[1]) > 0:
                print("Enter 'I' for the song information\nEnter 'L' to listen to the song\nEnter 'A' to add to a playlist\nHit ENTER to leave the selected song")
                uInput = input("> ")
                uInput = uInput.lower().strip()
                
                #set up a while loop here
                if uInput == 'i':
                   songInfo()
                elif uInput == 'L':
                    '''a listening event is recorded within the current session of the user (if a session has already started for the user) or within a new session (if not). 
                    When starting a new session, follow the steps given for starting a session. A listening event is recorded by either inserting a row to table listen or increasing the listen count in this table by 1''' 
                    print('fkn do something')
                elif uInput == 'a':
                    '''When adding a song to a playlist, the song can be added to an existing playlist owned by the user (if any) or to a new playlist.
                    When it is added to a new playlist, a new playlist should be created with a unique id (created by your system) and the uid set to the id of the user and a title should be obtained from input. '''
                    print('fkn do something')
                elif uInput == '':
                    break
                else:
                    print("Invalid input. Try again.")

                
            elif userInput[0] == 'playlist' and int(userInput[1]) > 0:
                
                q = '''SELECT s.sid, s.title, s.duration
                FROM playlists as p, songs as s, plinclude as pl
                WHERE  p.pid = pl.pid AND songs.sid = pl.sid
                '''
                cursor.execute(q)
                pSongs = cursor.fetcahll()
                connection.commit()
                
                for song in pSongs:
                    print(song)
            elif userInput[0] == 'd':
                #while index hasn't reached the end or over the array
                #print the next 5 and ask again
                while 1:
                    break


    elif userInput == 'a': 
        ''' ***TO DO: find artist by keywords. 
        
        The user should be able to provide one or more unique keywords, and the system should retrieve all artists that have any of those keywords either in their names 
        or in the title of a song they have performed. For each matching artist, the name, the nationality and the number of songs performed are returned. 
        The result should be ordered based on the number of matching keywords with artists that match the largest number of keywords listed on top. 
        If there are more than 5 matching artists, at most 5 matches will be shown at a time, letting the user either select a match for more information or see the rest of 
        the matches in a paginated downward format. The user should be able to select an artist and see the id, the title and the duration of all their songs. 
        Any time a list of songs are displayed, the user should be able to select a song and perform a song action as discussed next. 
        
        *** ''' 
        
        userInput = input("Please enter keywords to search for an artist by spaces only.\n>")

        keyWords = userInput.split()
        q = ''' 

        SELECT 
        FROM 
        WHERE

        '''
        cursor.execute(q)
        allMatching = cursor.fetchall()
        connection.commit()

        orderedList = orderByKW(allMatching, keyWords)

    elif userInput == 'e':
       endSess(sessNo)
       return

    return
def main():
    print("291 Mini-Project 1\n")
    #todo please check i spelled your names right lmao
    print("By Anya Hanatuke, Alinn Martinez, and Ayaan Jutt\n")
    #todo link database using URL
    global path
    connection, cursor = connect(path)
    quit = False
    while ~quit:
        initialDone = False
        while ~initialDone and ~quit:
            logReg = introLoop()
            if logReg == 'r':
                register()
                initialDone = True
            elif logReg == 'l':
                login(cursor)
                initialDone = True
            elif logReg == 'q':
                quit = True
                print("Thank you.")
                return

        sessionDone = False
        while ~sessionDone and ~quit:
            #todo uh oh this is the hard part
            break
main()
