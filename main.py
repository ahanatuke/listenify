""" NOTE: this file will only run if init_db.py has been run
    at least once. otherwise, tables are never created.
    This must be fixed before handing in. """
# todo fix

from operator import itemgetter
from audioop import add
import sqlite3
import getpass
import utilities

path = './291_proj'


def connect(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor


def introLoop():
    print("Press 'L' to login to an existing account.\nPress 'R' to register a new account.\nPress 'Q' to quit.")
    userInput = input("> ")
    userInput = userInput.lower().strip()
    while userInput != "r" and userInput != "l" and userInput != "q":
        print("Invalid input. Please try again.")
        userInput = input("> ")
        userInput = userInput.lower().strip()

    return userInput


def checkQuit(uInput):
    # TODO: @alinn check if it works
    if uInput.lower().strip() == 'q':
        print("Would you like to quit the program?")
        quit = input('> ')

        if quit:
            exit()


############################## REGISTER ###############################

def regInputs(suggestion, cursor):
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


def regSuccess(id, cursor):
    cursor.execute("""SELECT * FROM USERS WHERE uid LIKE ?""", (id,))
    if cursor.fetchone() is not None:
        print("You have successfully registered.")
        return True
    else:
        print("Registration was unsuccessful.")
        return False


def register():
    valid = True
    connection, cursor = connect(path)
    q = '''SELECT *
    FROM users
    '''
    cursor.execute(q)

    usersAmount = len(cursor.fetchall())
    # connection.commit()

    # this functionality is probably unnecessary and yet, i did it anyway
    usersAmount += 1
    suggestion = "u" + str(usersAmount)
    cursor.execute('''SELECT * FROM users WHERE uid=?''', (suggestion,))
    while cursor.fetchone() is not None:
        usersAmount += 1
        suggestion = "u" + str(usersAmount)
        cursor.execute('''SELECT * FROM users WHERE uid=?''', (suggestion,))

    inputU, inputN, inputP = regInputs(suggestion, cursor)

    reEnter = input("Keep the following [Y/N]?: \n" + inputU + "\n" + inputN + " \n(Press enter to cancel) ")
    check = False

    while check == False:

        if reEnter.lower().strip() == 'n':
            print("Your information has been discarded.")
            inputU, inputN, inputP = regInputs(suggestion, cursor)
            break
        elif reEnter.lower().strip() == 'y':
            q = '''INSERT INTO users 
            VALUES ((?), (?), (?))'''
            cursor.execute(q, (inputU, inputN, inputP))
            connection.commit()
            valid = regSuccess(inputU, cursor)
            break
        elif reEnter == "":
            valid = False
            inputU = ""
            break
        else:
            print("Invalid input. Please try again.")
            reEnter = input("Keep the following [Y/N]?: \n" + inputU + "\n" + inputN + " \n(Press enter to cancel) ")

    return valid, inputU


############################## END OF REGISTER ###############################


def idCheck(id, cursor):
    user = False
    artist = False
    cursor.execute("""SELECT * FROM USERS WHERE uid LIKE ?""", (id,))
    if cursor.fetchone() is not None:
        user = True
    cursor.execute("""SELECT * FROM artists WHERE aid LIKE ?""", (id,))
    if cursor.fetchone() is not None:
        artist = True
    return user, artist


def userPwd(id, cursor):
    print("Please enter the password for your user account, or press enter to exit.")
    while True:
        pwd = getpass.getpass("> ")
        if pwd == "":
            return False
        cursor.execute("SELECT * FROM USERS WHERE uid LIKE ? AND pwd=?", (id, pwd))
        if cursor.fetchone() != None:
            return True
        else:
            print("Incorrect password: please try again or press enter to exit.")


def artistPwd(id, cursor):
    print("Please enter the password for your artist account, or press enter to exit.")
    while True:
        pwd = getpass.getpass("> ")
        if pwd == "":
            return False
        cursor.execute("SELECT * FROM artists WHERE aid LIKE ? AND pwd=?", (id, pwd))
        if cursor.fetchone() != None:
            return True
        else:
            print("Incorrect password: please try again or press enter to exit.")


############################## LOGIN ###############################
def endProg(): 
    userInput = input("Would you like to close the program? [Y/N]\n> ")
    userInput = userInput.lower().strip()
    if userInput == 'y':
        exit()
    elif userInput == 'n':
        return
    else:
        userInput = input("Invalid input, please try again.\nWould you like to close the program? [Y/N]\n> ").lower().split()


def login(cursor):
    """Login: nested loop unfortunately get ready for this to run in O(n^2)"""
    success = False
    valid = True
    uid = ""
    pwd = ""

    loginType = ""
    user, artist = False, False
    while success == False and valid == True:

        uidSuccess = False
        print("Please enter your User ID, or press enter to exit:")
        while uidSuccess == False and valid == True:
            uid = input("> ")
            if uid == "":
                valid = False
                break

            user, artist = idCheck(uid, cursor)
            if user == False and artist == False:
                print("No user with that username. Please try again, or press enter to exit.")
                break
            elif user == True and artist == False:
                loginType = "user"
                break
            elif user == False and artist == True:
                loginType = "artist"
                break
            elif user == True and artist == True:
                print("Press 'A' to login as an artist. Press 'U' to login as a user.")
                while True:
                    loginTypeInput = input("> ")
                    if loginTypeInput.lower().strip() == 'a':
                        loginType = "artist"
                        break
                    elif loginTypeInput.lower().strip() == 'u':
                        loginType = "user"
                        break
                    else:
                        print("Invalid input. Please try again.")

                break

        pwdSuccess = False
        if valid == True:
            print("Please enter the password for user %s, or press enter to change user" % uid)
            if loginType == "user":
                pwdSuccess = userPwd(uid, cursor)
            elif loginType == "artist":
                pwdSuccess = artistPwd(uid, cursor)

        if pwdSuccess == True:
            break

    return valid, uid, loginType


############################## END OF LOGIN #########################


############################## ARTIST ###############################
def addSong(artist):
    """CONCEPT: ask for title and duration as inputs get all songs and create a new sid by adding length of all songs
    + 1 from there see if we can select a song from the input provided by the artist a song provided by the artist
    should be unique, and therefore if we check the len of songExist we should get a len of 0 If the song doesn't
    exist we insert it, and then request an input about whom the features are, once provided do a for loop and add
    every feature Make sure to confirm that is either added in or exists"""

    # TODO: check if it works

    connection, cursor = connect(path)

    # get all songs and get len
    q = '''SELECT *
            FROM songs as s'''
    cursor.execute(q)
    sidNew = len(cursor.fetchall()) + 1
    connection.commit()

    print("Please enter the title and duration (in seconds): ")
    title = input("Title: ")
    duration = input("Duration (in seconds): ")
    duration = int(duration)

    # CHECK IF THE SONG EXISTS
    q = '''SELECT  s.title, s.duration
        FROM songs as s, artists as a, perform as p
        WHERE s.title = ? AND s.duration = ? AND a.aid = ? AND p.sid = s.sid AND p.aid = a.aid 
        '''
    cursor.execute(q, (title, duration, artist,))
    # 1 song should exist like this, len of fetchone = 0 it should be unique HYPOTHETICALLY
    songExist = cursor.fetchone()
    connection.commit()

    if songExist == None:

        q = '''INSERT INTO songs 
        VALUES(?, ?, ?)'''
        cursor.execute(q, (sidNew, title, duration,))
        connection.commit()
        userInput = input("Please list the aid's of everyone who is featured on your song (hit ENTER if none): ")
        inputChecker = userInput.split()
        if inputChecker != '':
            result = [x.strip() for x in userInput.split(',')]
            # assuming we dont need to validate aids for every feature
            for feature in result:
                q = '''INSERT INTO perform 
                VALUES (?, ?)'''
                cursor.execute(q, (feature, sidNew))
                connection.commit()
        print("Song %s has been successfully added in." % songExist)


    else:
        print("Cannot add, this song already exists.")

    return


def topListen(artist):
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
    """TODO: check if it works, add a way to logout"""
    # artist is an aid of the user who logged in, used to check if a song exists or not
    connection, cursor = connect(path)
    print(
        "Enter 'S' to add a song.\nEnter 'F' to find your top listeners and playlists with most of your songs.\nEnter "
        "'L' to logout.\nEnter 'E' to exit the program.")
    userInput = input("> ")
    userInput = userInput.lower().strip()

    check = True

    while check == True:


        if userInput != "s" and userInput != "f" and userInput != 'l' and userInput != 'e':

            print("Invalid input. Please try again.")
            userInput = input("> ")
            userInput = userInput.lower().strip()
        elif userInput == 's':
            addSong(artist)
        elif userInput == 'f':
            topListen(artist)
        elif userInput == 'l':
            userInput = input("Are you sure you want to logout? [Y/N]\n> ").lower().strip()
            if userInput == 'y':
                check = False
                return True
            elif userInput == 'n':
                print(
                    "Enter 'S' to add a song.\nEnter 'F' to find your top listeners and playlists with most of your songs.\nEnter 'L' to logout.\nEnter 'E' to exit the program.")
                userInput = input("> ").lower().strip()
        elif userInput == 'e':
            endProg()

    return True


############################## END OF ARTIST ###############################


############################## USER ###############################
def startSess():
    """TODO: Check if it works"""

    connection, cursor = connect(path)

    # get all sessions and add 1 to get a next sno
    q = '''SELECT *
        FROM sessions'''
    cursor.execute(q)
    newSession = len(cursor.fetchall()) + 1
    connection.commit()

    # add the session in
    q = '''
    INSERT INTO sessions(sno, start, end)
    VALUES(?, datetime('now'), NULL)
    '''
    cursor.execute(q, (newSession,))
    connection.commit()

    return newSession


def endSess(sessNo):
    """TODO: Check if it works"""

    connection, cursor = connect(path)
    q = '''INSERT INTO sessions(end)
    VALUES(datetime('now'))
    WHERE sessions.sno = ?'''
    cursor.execute(q, (sessNo))
    connection.commit()

    return





def songInfo(song):

    """ Finish the query """

    # get artist name, sid, title and duration + any playlist the song is in

    connection, cursor = connect(path)
    q = '''SELECT a.name, s.sid, s.title, s.duration, pl.title 
    FROM artists a, perform pf, songs s, playlists pl, plinclude pli
    WHERE a.aid = pf.aid
    AND pf.sid = ?
    OR (pli.sid = ?)'''
    cursor.execute(q, (song,))
    songInfo = cursor.fetchone()
    connection.commit()

    for info in songInfo:
        print(info)



def addToPlaylist(sessNo, userInput, user):
    connection, cursor = connect(path)
    #todo: just pass the cursor, don't do this

    q = '''SELECT s.sid 
    FROM songs as s
    WHERE s.sid = ?'''
    cursor.execute(q, userInput[1])
    sid = cursor.fetchone()
    connection.commit()
    uInput = input("Enter 'N' to insert this into a new playlist\nEnter 'A' to add into an existing playlist\n> ").lower().strip()
    if uInput == 'n':
        q = '''SELECT *
        from playlists'''
        cursor.execute(q)
        sumPl = len(cursor.fetchall()) + 1
        connection.commit()
        
        pInput = input("Enter a title for your playlist\n> ").lower().strip()

        q =  '''INSERT INTO playlists
        VALUES (?, ?, ?)'''
        cursor.execute(q, (sumPl, pInput, user))
        connection.commit()
        q = '''INSERT INTO plinclude
        VALUES (?, ?, ?)'''
        cursor.execute(q, (sumPl, sid[0], sessNo ))
        connection.commit()
    elif uInput == 'a':
        print("Select the playlist id you would like to add")
        i = input("> ").lower().strip()
        q = '''SELECT p.pid
        FROM playlists as p, users as u
        WHERE p.pid = ? and u.uid = ?'''
        cursor.execute(q, (i, user))
        playlist = cursor.fetchone()
        if playlist == None:
            print("Invalid playlist, try again.")
        else: 
            q = '''INSERT INTO plinclude
            VALUES (?, ?, ?)'''
            cursor.execute(q, (playlist[0], sid, sessNo))
        
    return

def displayPlaylist():
    connection, cursor = connect(path)
    q = '''SELECT s.sid, s.title, s.duration
                FROM playlists as p, songs as s, plinclude as pl
                WHERE  p.pid = pl.pid AND songs.sid = pl.sid
                '''
    cursor.execute(q)
    pSongs = cursor.fetchall()
    connection.commit()

    for song in pSongs:
        print(song)

def goDown(allMatchingL, index):
    for i in range(len(allMatchingL) - index):
        if  i >= 5 or allMatchingL[index] == None:
            return
        else:
            print(allMatchingL[index])
            index += 1

def user(user):
    """LOTS TO DO:
    ***___*** => things to start on
    """
    # user is an uid of the user to logged in
    connection, cursor = connect(path)
    sessionStarted = False
    loggedIn = True
    while(loggedIn):
        print(
        "To start a session enter 'S'\nTo search for a song or playlist enter 'P'\nEnter 'A' to search for an "
        "artist\nTo end the session enter 'D'\nTo logout enter 'L'\nTo exit the program press 'E'  ")
        userInput = input("> ")
        userInput = userInput.lower().strip()

        if userInput == 's':
            sessNo = startSess()
            sessionStarted = True
        elif userInput == 'p':
            # " user should be able to provide one or more unique keywords,"
            # FOCUS ON: Either having it be one input split into an array or requesting multiple inputs for keywords (probably the best????)
            # must indicate if playlist or song is displayed

            userInput = input("Please enter keywords to search for playlists or songs by spaces only.\n>")

            # get the keywords into an array
            keyWords = userInput.split()
            '''*** TO DO: get the rows, even if they're unordered thats okay we'll sort it in orderbyKW() *** '''
            # get all matching rows from keywords
            # any not all

            songResults = []
            playlistResults = []
            i=0
            for word in keyWords:
                cursor.execute("""SELECT s.sid, s.title, s.duration
                                    FROM songs as s
                                    WHERE s.title LIKE ? """, ("%" + word.strip().lower() + "%",))


                matchedSongs = cursor.fetchall()
                for song in matchedSongs:
                    i += 1
                    print(i)
                    song = list(song)
                    inMatched = False
                    if len(songResults)==0:
                        result = [song, 1, 0,i]
                        songResults.append(result)
                    else:
                        for result in songResults:
                            if result == song:
                                result[1] += 1
                                inMatched = True
                                break

                        if inMatched == False:
                            result = [song, 1, 0,i]
                            songResults.append(result)


                cursor.execute("""SELECT p.pid, p.title
                                    FROM playlists as p
                                    WHERE p.title LIKE ? """, ("%" + word.strip().lower() + "%",))
                #todo get total duration

                matchedPlaylists = cursor.fetchall()
                for playlist in matchedPlaylists:
                    i += 1

                    playlist = list(playlist)
                    inMatched = False
                    if len(playlistResults)==0:
                        result = [playlist, 1, 1, i]
                        playlistResults.append(result)
                    else:
                        for result in playlistResults:
                            if result == playlist:
                                result[1] += 1
                                inMatched = True
                                break

                        if inMatched == False:
                            result = [playlist, 1, 1, i]
                            playlistResults.append(result)

            for playlist in playlistResults:
                songResults.append(playlist)

            results = sorted(songResults, key=lambda p: p[1])

            items = []
            for i in range(len(songResults)):
                items.append(results[i][0])
            print(items)

            selectedItem = utilities.paginate(items)
            if selectedItem == None:
                #todo fix me make all this a fxn n do a return
                pass
            elif results[selectedItem][2]== 0:
                #todo its a song do the song thing
                pass
            elif results[selectedItem][2] == 1:
                #todo its a playlist do the playlist thing
                pass


            ''' *** TO DO: find a way to distinguish btwn playlist and song and how to enter a specific one*** 
            one thing to note is that neither song or playlist has a letter to distinguish itself as an id
                    i.e. sid of wavin flag would be 1 and not s1
            ways to solve this: maybe look into finding a way within the for loop to attach an s or a p to the id?
            only playlists have users, and only song have duration, look into that or other ways to distinguish whats a playlist. 
        '''
            
            check = True
            while (check):
                print(
                "Enter the id of a playlist or song you want to select as (playlist/song [number])\nEnter 'N' to go to "
                "the next 5\Hit 'ENTER' to leave")
                userInput = input("> ")
                userInput = userInput.lower().strip()
                # leave
                if userInput[0] == '':
                    check = False

                # focus on getting song1 to see what the user inputs is a song or a playlist
                elif userInput[0] == 'song' and int(userInput[1]) > 0:
                    print(
                        "Enter 'I' for the song information\nEnter 'L' to listen to the song\nEnter 'A' to add to a "
                        "playlist\nHit ENTER to leave the selected song")
                    uInput = input("> ")
                    uInput = uInput.lower().strip()

                    # set up a while loop here
                    if uInput == 'i':
                        songInfo()
                    elif uInput == 'L':
                        '''a listening event is recorded within the current session of the user (if a session has already 
                        started for the user) or within a new session (if not). When starting a new session, follow the 
                        steps given for starting a session. A listening event is recorded by either inserting a row to 
                        table listen or increasing the listen count in this table by 1 '''

                        q = '''SELECT s.sid 
                        FROM songs as s
                        WHERE s.sid = ?'''
                        cursor.execute(q, userInput[1])
                        sid = cursor.fetchone()
                        connection.commit()

                        if sessionStarted:
                            q = '''UPDATE listen
                            SET listen.count = listen.count + 1
                            WHERE listen.uid = ? AND listen.sno = ? AND listen.sid = ?'''
                            cursor.execute(q, (user, sessNo, sid[0],))
                            connection.commit()
                        else:
                            sessNo = startSess()
                            sessionStarted = True
                            q = '''INSERT INTO listen
                            VALUES(?, ?, ?, ?)'''
                            cursor.execute(q, (user, sessNo, sid, 1,))
                            connection.commit()             

                    elif uInput == 'a':
                        '''When adding a song to a playlist, the song can be added to an existing playlist owned by the 
                        user (if any) or to a new playlist. When it is added to a new playlist, a new playlist should be 
                        created with a unique id (created by your system) and the uid set to the id of the user and a 
                        title should be obtained from input. '''

                        addToPlaylist(sessNo, userInput[1], user)
                    elif uInput == '':
                        break
                    else:
                        print("Invalid input. Try again.")


                elif userInput[0] == 'playlist' and int(userInput[1]) > 0:
                    displayPlaylist()
                    
                elif userInput[0] == 'd':
                    # while index hasn't reached the end or over the array
                    # print the next 5 and ask again
                    
                    index = goDown(allMatchingL, index)


        elif userInput == 'a':
            ''' ***TO DO: find artist by keywords. 
            
            The user should be able to provide one or more unique keywords, and the system should retrieve all artists 
            that have any of those keywords either in their names or in the title of a song they have performed. For each 
            matching artist, the name, the nationality and the number of songs performed are returned. The result should 
            be ordered based on the number of matching keywords with artists that match the largest number of keywords 
            listed on top. If there are more than 5 matching artists, at most 5 matches will be shown at a time, 
            letting the user either select a match for more information or see the rest of the matches in a paginated 
            downward format. The user should be able to select an artist and see the id, the title and the duration of 
            all their songs. Any time a list of songs are displayed, the user should be able to select a song and perform 
            a song action as discussed next. 
            
            *** '''

            userInput = input("Please enter keywords to search for an artist by spaces only.\n>")

            keyWords = userInput.split()
            q = ''' 
            SELECT a.name, a.nationality, COUNT(s.sid)
            FROM songs as s, artasts as a, perform as p
            WHERE s.sid = p.sid AND a.aid = p.aid AND ((s.title LIKE ? AND  a.name LIKE ?) OR s.title LIKE ? OR a.name LIKE ?)
            '''
            cursor.execute(q, (keyWords[0], keyWords[1], keyWords[0], keyWords[1],))
            allMatching = cursor.fetchall()
            connection.commit()

            orderedList = orderByKW(allMatching, keyWords)

        elif userInput == 'd':
            endSess(sessNo)
            sessionStarted = False
            
        elif userInput == 'l':
            check = True
            while check: 
                userInput = input("Are you sure you want to logout? [Y/N]\n> ").lower().strip()
                if userInput == 'y':
                    loggedIn = False
                    return True
                elif userInput == 'n':
                    print(
                    "To start a session enter 'S'\n To search for a song or playlist enter 'P'\nEnter 'A' to search for an "
                    "artist\nTo end the session enter 'D'\nTo logout enter 'L'\nTo exit the program press 'E'  ")
                    userInput = input("> ").lower().split()
                else:
                    print("Invalid input, try again.")
        elif userInput == 'e':
            endProg()
    return True


############################## END OF USER ###############################


def main():
    print("291 Mini-Project 1\n")

    print("By Anya Hanatuke, Alinn Martinez, and Ayaan Jutt\n")
    # todo link database using URL
    global path
    connection, cursor = connect(path)

    quitProgram = False
    userTitle = ""

    while quitProgram == False:
        initialDone = False
        while initialDone == False and quitProgram == False:

            logReg = introLoop()
            if logReg == 'r':
                valid, uid = register()
                if valid:
                    initialDone = True
            elif logReg == 'l':
                valid, uid, userTitle = login(cursor)
                if valid:
                    initialDone = True

            elif logReg == 'q':
                quitProgram = True
                print("Thank you.")
                break

        sessionDone = False

        while sessionDone == False and quitProgram == False:

            if userTitle == 'artist':
                sessionDone = artist(id)
                sessionDone = True
            elif userTitle == 'user':
                sessionDone = user(id)
                sessionDone = True


main()


#todo register hangs after registration, fix (registration successful just stop it from hanging)
#todo login does a weird print, fix
