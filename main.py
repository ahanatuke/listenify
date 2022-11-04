""" NOTE: this file will only run if init_db.py has been run
    at least once. otherwise, tables are never created.
    This must be fixed before handing in. """
# todo fix

from audioop import add
from logging import exception
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
        print("Would you like to quit the program? [Y/N]")
        quit = input('> ')

        if quit.lower().strip() == 'y':
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


def register(cursor, connection):
    valid = True
    q = '''SELECT *
    FROM users
    '''
    cursor.execute(q)

    usersAmount = len(cursor.fetchall())

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


############################## LOGIN ###############################

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
    print(
        "Please enter the password for user %s, or press enter change user or 'Q' to quit program." % id)  # TODO: add quit func, checkQuit() OR  have it return back to first screen
    while True:
        pwd = getpass.getpass("> ")
        if pwd == "":
            return False
        cursor.execute("SELECT * FROM USERS WHERE uid LIKE ? AND pwd=?", (id, pwd))
        if cursor.fetchone() != None:
            return True
        else:
            print("Incorrect password: please try again or press enter to exit.")  # TODO: checkQuit()


def artistPwd(id, cursor):
    print("Please enter the password for your artist account, or press enter to exit.")  # TODO: checkQuit()
    while True:
        pwd = getpass.getpass("> ")
        if pwd == "":
            return False
        cursor.execute("SELECT * FROM artists WHERE aid LIKE ? AND pwd=?", (id, pwd))
        if cursor.fetchone() != None:
            return True
        else:
            print("Incorrect password: please try again or press enter to exit.")  # TODO: checkQuit()


def endProg():
    userInput = input("Would you like to close the program? [Y/N]\n> ")
    userInput = userInput.lower().strip()
    if userInput == 'y':
        exit()
    elif userInput == 'n':
        return
    else:
        userInput = input(
            "Invalid input, please try again.\nWould you like to close the program? [Y/N]\n> ").lower().split()


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
        print("Please enter your User ID, or press enter to exit:")  # TODO: checkQuit()
        while uidSuccess == False and valid == True:
            uid = input("> ")
            if uid == "":
                valid = False
                break

            user, artist = idCheck(uid, cursor)
            if user == False and artist == False:
                print("No user with that username. Please try again, or press enter to exit.")  # TODO: checkQuit()
                break
            elif user == True and artist == False:
                loginType = "user"
                break
            elif user == False and artist == True:
                loginType = "artist"
                break
            elif user == True and artist == True:  # TODO: never hits this line when logging in as artist
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
            if loginType == "user":
                pwdSuccess = userPwd(uid, cursor)
            elif loginType == "artist":
                pwdSuccess = artistPwd(uid, cursor)

        if pwdSuccess == True:
            break

    return valid, uid, loginType


############################## END OF LOGIN #########################


############################## ARTIST ###############################
def addSong(artist, cursor, connection):
    """CONCEPT: ask for title and duration as inputs get all songs and create a new sid by adding length of all songs
    + 1 from there see if we can select a song from the input provided by the artist a song provided by the artist
    should be unique, and therefore if we check the len of songExist we should get a len of 0 If the song doesn't
    exist we insert it, and then request an input about whom the features are, once provided do a for loop and add
    every feature Make sure to confirm that is either added in or exists"""

    # TODO: check if it works

    # get all songs and get len
    q = '''SELECT *
            FROM songs as s'''
    cursor.execute(q)
    sidNew = len(cursor.fetchall()) + 1

    cursor.execute('''SELECT * FROM songs WHERE sid=?''', (sidNew,))

    while cursor.fetchone() is not None:
        sidNew += 1
        cursor.execute('''SELECT * FROM sid WHERE sid=?''', (sidNew,))

    print("Please enter the following song information: ")
    title = input("Title: ")
    duration = input("Duration (in seconds): ")  # TODO: hangs after entering seconds
    check = True
    while (check):
        try:
            duration = int(duration)
            if duration < 0:
                raise Exception
            check = True
        except:
            print("Invalid number please try again.")
            duration = input("Duration (in seconds): ")
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
            # assuming we don't need to validate aids for every feature
            for feature in result:
                q = '''INSERT INTO perform 
                VALUES (?, ?)'''
                cursor.execute(q, (feature, sidNew))
                connection.commit()
        print("Song %s has been successfully added in." % songExist)


    else:
        print("This song already exists, would you like to add it again? [Y/N/E to close program] ")
        userInput = input("> ").lower.strip()
        if userInput == 'y':
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
        elif userInput == 'n':
            print("Song has not been added in.")
            return
        elif userInput == 'e':
            endProg()
    return


def topListen(artist, cursor, connection):
    q = '''SELECT DISTINCT u.uid, a.name
    FROM users u, sessions ses, listen l, artists a, perform p, songs s
    WHERE ses.uid = l.uid
        AND l.sid = p.sid
        AND p.aid = a.aid
        AND a.aid = 'a1'
    ORDER BY l.cnt DESC
    LIMIT 3
    '''
    cursor.execute(q)
    top3U = cursor.fetchall()
    connection.commit()
    for user in top3U:
        print(user)

    q = '''SELECT DISTINCT pl.title, a.name
    FROM playlists pl, artists a
    WHERE (SELECT DISTINCT MAX(s.sid)
        FROM perform p,
                songs s,
                plinclude pi, 
                playlists pl2
        WHERE a.aid = 'a1'
             AND p.sid = s.sid
            AND pi.sid = s.sid
            AND a.aid = p.aid
        ORDER BY pl2.pid DESC)
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
        "Enter 'S' to add a song.\nEnter 'F' to find your top listeners and playlists with most of your songs.\nEnter "  # TODO: change S to A
        "'L' to logout.\nEnter 'E' to exit the program.")  # TODO: checkQuit()
    userInput = input("> ")
    userInput = userInput.lower().strip()

    check = True

    while check == True:

        if userInput != "s" and userInput != "f" and userInput != 'l' and userInput != 'e':

            print("Invalid input. Please try again.")
            userInput = input("> ")
            userInput = userInput.lower().strip()
        elif userInput == 's':  # TODO: change S to A
            addSong(artist, cursor, connection)
        elif userInput == 'f':
            topListen(artist, cursor, connection)
        elif userInput == 'l':
            userInput = input("Are you sure you want to logout? [Y/N]\n> ").lower().strip()
            if userInput == 'y':
                check = False
                return True
            elif userInput == 'n':
                print(
                    "Enter 'S' to add a song.\nEnter 'F' to find your top listeners and playlists with most of your songs.\nEnter 'L' to logout.\nEnter 'E' to exit the program.")  # TODO: change S to A
                userInput = input("> ").lower().strip()  # TODO: checkQuit()
        elif userInput == 'e':
            endProg()

    return True


############################## END OF ARTIST ###############################


############################## USER ###############################
def startSess(cursor, connection):
    """TODO: Check if it works"""

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


def endSess(sessNo, cursor, connection):
    """TODO: Check if it works"""

    q = '''INSERT INTO sessions(end)
    VALUES(datetime('now'))
    WHERE sessions.sno = ?'''  # TODO: syntax error operational error near "WHERE"
    cursor.execute(q, (sessNo,))
    connection.commit()

    return


def songInfo(song, cursor, connection):
    # song = sid
    """ Finish the query """

    # get artist name, sid, title and duration + any playlist the song is in

    connection, cursor = connect(path)
    q = '''SELECT a.name, s.sid, s.title, s.duration, pl.title 
    FROM artists a, perform pf, songs s, playlists pl, plinclude pli
    WHERE a.aid = pf.aid
    AND pf.sid = ?
    AND pli.sid = ?
    AND pli.pid = pl.pid'''
    cursor.execute(q, (song[0], song[0]))
    songInfo = cursor.fetchone()
    connection.commit()

    for info in songInfo:
        print(info)


def addToPlaylist(sessNo, userInput, user, cursor, connection):
    # todo: just pass the cursor, don't do this

    q = '''SELECT s.sid 
    FROM songs as s
    WHERE s.sid = ?'''
    cursor.execute(q, userInput[
        1])  # TODO: error incorrect number of bindings supplied. current statment uses 1, and there are 6 supplied
    sid = cursor.fetchone()
    connection.commit()
    uInput = input(
        "Enter 'N' to insert this into a new playlist\nEnter 'A' to add into an existing playlist\n> ").lower().strip()
    if uInput == 'n':  # TODO: error Incorrect number of bindings supplied. The current statement uses 1, and there are 6 supplied
        q = '''SELECT *
        from playlists'''
        cursor.execute(q)
        sumPl = len(cursor.fetchall()) + 1
        connection.commit()

        pInput = input("Enter a title for your playlist\n> ").lower().strip()

        q = '''INSERT INTO playlists
        VALUES (?, ?, ?)'''
        cursor.execute(q, (sumPl, pInput, user))
        connection.commit()
        q = '''INSERT INTO plinclude
        VALUES (?, ?, ?)'''
        cursor.execute(q, (sumPl, sid[0], sessNo))
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


def displayPlaylist(plID, cursor, connection):
    q = '''SELECT s.sid, s.title, s.duration
                FROM playlists as p, songs as s, plinclude as pl
                WHERE  p.pid = pl.pid AND s.sid = pl.sid AND p.pid = ?
                '''
    cursor.execute(q, (plID,))
    pSongs = cursor.fetchall()
    connection.commit()
    index = 0
    for song in pSongs:
        print(song)

    print("Enter a song ID for more information or press enter to exit")  # TODO: checkQuit()
    while True:
        userInput = input("> ")
        if userInput == "":
            return
        for s in pSongs:
            if userInput.strip().lower() == str(s[0]):
                return int(userInput)

        print("Invalid input, please try again")


def orderByKWP(cursor, keyWords):
    songResults = []
    playlistResults = []
    i = 0
    for word in keyWords:
        cursor.execute("""SELECT s.sid, s.title, s.duration
                            FROM songs as s
                            WHERE s.title LIKE ? """, ("%" + word.strip().lower() + "%",))

        matchedSongs = cursor.fetchall()
        for song in matchedSongs:
            i += 1
            song = list(song)
            song.append("Song")
            inMatched = False
            if len(songResults) == 0:
                result = [song, 1, 0, i]
                songResults.append(result)
            else:
                for result in songResults:
                    if result == song:
                        result[1] += 1
                        inMatched = True
                        break

                if inMatched == False:
                    result = [song, 1, 0, i]
                    songResults.append(result)

        cursor.execute("""SELECT p.pid, p.title
                            FROM playlists as p
                            WHERE p.title LIKE ? """, ("%" + word.strip().lower() + "%",))
        # todo get total duration

        matchedPlaylists = cursor.fetchall()
        for playlist in matchedPlaylists:
            i += 1

            playlist = list(playlist)
            q = '''SELECT SUM(s.duration)
            FROM songs as s, plinclude as pl, playlists as p 
            WHERE p.pid = ? AND pl.pid = ? and s.sid = pl.sid  
            '''
            cursor.execute(q, (playlist[0], playlist[0],))

            sum = cursor.fetchone()

            playlist.append(sum)
            playlist.append("Playlist")

            inMatched = False
            if len(playlistResults) == 0:
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

    return results, items


def displayArtist(cursor, aid):
    q = '''SELECT s.sid, s.title, s.duration
                FROM songs as s, perform as p
                WHERE  p.aid = ? AND s.sid = p.sid
                '''
    cursor.execute(q, (aid,))
    pSongs = cursor.fetchall()

    for song in pSongs:
        print(song)


def selectSong(sid, sessNo, sessionStarted, cursor, connection):
    print(
        "Enter 'I' for the song information\nEnter 'L' to listen to the song\nEnter 'A' to add to a "
        "playlist\nHit ENTER to leave the selected song")
    uInput = input("> ")
    uInput = uInput.lower().strip()

    # set up a while loop here
    if uInput == 'i':

        # FIRST ARG IS SONG, RETRIEVE THE SONG FIRST
        songInfo(sid, cursor, connection)
    elif uInput == 'L':
        '''a listening event is recorded within the current session of the user (if a session has already 
        started for the user) or within a new session (if not). When starting a new session, follow the 
        steps given for starting a session. A listening event is recorded by either inserting a row to 
        table listen or increasing the listen count in this table by 1 '''

        q = '''SELECT s.sid 
        FROM songs as s
        WHERE s.sid = ?'''
        cursor.execute(q, sid)
        song = cursor.fetchone()
        connection.commit()

        if sessionStarted:
            q = '''UPDATE listen
            SET listen.count = listen.count + 1
            WHERE listen.uid = ? AND listen.sno = ? AND listen.sid = ?'''
            cursor.execute(q, (user, sessNo, song[0],))
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

        addToPlaylist(sessNo, sid, user, cursor, connection)
    else:
        print("Invalid input. Try again.")
    return


def user(user):
    """LOTS TO DO:
    ***___*** => things to start on
    """
    # user is an uid of the user to logged in
    connection, cursor = connect(path)
    sessionStarted = False
    loggedIn = True
    while (loggedIn):
        print(
            "To start a session enter 'S'\nTo search for a song or playlist enter 'P'\nTo search for an artist enter 'A' "
            "\nTo end the session enter 'D'\nTo logout enter 'L'\nTo exit the program press 'E'  ")  # TODO: remove end session and move to after session starts # TODO: perhaps update the exit program with quit and use checkQuit()
        userInput = input("> ")
        userInput = userInput.lower().strip()  # TODO: doesn't seem to overwrite at times??
        sessNo = 0
        if userInput == 's':
            sessNo = startSess(cursor, connection)
            sessionStarted = True
        elif userInput == 'p':
            # " user should be able to provide one or more unique keywords,"
            # FOCUS ON: Either having it be one input split into an array or requesting multiple inputs for keywords (probably the best????)
            # must indicate if playlist or song is displayed

            userInput = input("Please enter keywords to search for playlists or songs by spaces only.\n> ")

            # get the keywords into an array
            keyWords = userInput.split()
            '''*** TO DO: get the rows, even if they're unordered thats okay we'll sort it in orderbyKW() *** '''
            # get all matching rows from keywords
            # any not all

            results, items = orderByKWP(cursor, keyWords)

            selectedItem = utilities.paginate(items)

            if selectedItem == None:
                pass
            elif results[selectedItem][2] == 0:
                sid = results[selectedItem][0]

                selectSong(sid, sessNo, sessionStarted, cursor, connection)


            elif results[selectedItem][2] == 1:
                pid = str(results[selectedItem][0][0])
                print(pid)
                sid = displayPlaylist(pid, cursor, connection)

                while True:
                    if sid == None:
                        break
                    elif cursor.execute("""SELECT * FROM songs WHERE sid = ?""", (sid,)).fetchone() != None:
                        selectSong(sid, cursor, connection)
                        break
                    else:
                        print("Invalid Input, please try again")
                        sid = input("> ")

            ''' *** TO DO: find a way to distinguish btwn playlist and song and how to enter a specific one*** 
            one thing to note is that neither song or playlist has a letter to distinguish itself as an id
                    i.e. sid of wavin flag would be 1 and not s1
            ways to solve this: maybe look into finding a way within the for loop to attach an s or a p to the id?
            only playlists have users, and only song have duration, look into that or other ways to distinguish whats a playlist. 
        '''





        elif userInput == 'a':
            # TODO: find artist by keywords.
            ''' ***TODO: find artist by keywords. 
            
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
            for word in keyWords:
                q = ''' 
                SELECT a.name, a.nationality, COUNT(s.sid)
                FROM songs as s, artists as a, perform as p
                WHERE s.sid = p.sid AND a.aid = p.aid AND (s.title LIKE ? OR a.name LIKE ?)
                GROUP BY a.aid
                '''
                cursor.execute(q, ("%" + word.lower().strip() + "%", "%" + word.lower().strip() + "%"))
                allMatching = cursor.fetchall()

                artistResults = []
                i = 0
                for artist in allMatching:
                    i += 1
                    artist = list(artist)
                    inMatched = False
                    if len(artistResults) == 0:
                        result = [artist, 1, i]
                        artistResults.append(result)
                    else:
                        for result in artistResults:
                            if result == artist:
                                result[1] += 1
                                inMatched = True
                                break

                        if inMatched == False:
                            result = [artist, 1, i]
                            artistResults.append(result)

                results = sorted(artistResults, key=lambda p: p[1])

                items = []
                for i in range(len(artistResults)):
                    items.append(results[i][0])

                selectedArtist = utilities.paginate(items)

                if selectedArtist == None:
                    pass
                # todo do the quit, call checkQuit()
                else:
                    artist = items[selectedArtist]
                    cursor.execute("""SELECT aid FROM artists WHERE name = ? AND nationality = ?""",
                                   (artist[0], artist[1]))
                    aid = str(cursor.fetchone()[0])

                    displayArtist(cursor, aid)
                    print("Enter song id to see more info, or press Enter to quit")  # TODO: also use checkQuit()
                    sid = input("> ")
                    if sid == None:
                        pass  # todo the quit thing, call checkQuit()
                    else:
                        while True:
                            cursor.execute('''SELECT * FROM songs WHERE sid = ?''', (sid,))
                            if cursor.fetchone() == None:
                                print("Invalid input, please try again")
                                sid = input("> ")
                            else:
                                selectSong(sid, cursor, connection)



        elif userInput == 'd':  # TODO: move to after session starts
            endSess(sessNo, cursor, connection)
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
    # global path
    # TODO: we have no way of checking if they give us a valid database
    path = input("Please enter a database\n> ")
    path = './' + path

    connection, cursor = connect(path)

    quitProgram = False
    userTitle = ""

    while quitProgram == False:
        initialDone = False
        while initialDone == False and quitProgram == False:

            logReg = introLoop()
            if logReg == 'r':
                valid, uid = register(cursor)
                if valid:
                    initialDone = True
            elif logReg == 'l':
                valid, id, userTitle = login(cursor)
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

# todo register hangs after registration, fix (registration successful just stop it from hanging)
