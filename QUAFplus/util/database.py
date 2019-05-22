import sqlite3, random

def createPosts():
    db = sqlite3.connect("data/quaf.db")
    c = db.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS posts(
                postId INTEGER PRIMARY KEY AUTOINCREMENT,
                postType TEXT,
                postInfo TEXT,
                authorID INTEGER,
                tags TEXT
                )"""
                )
    c.execute("""CREATE TABLE IF NOT EXISTS replies(
                replyID INTEGER,
                replyContent TEXT,
                parentID INTEGER,
                authorID INTEGER
                )"""
                )

    c.execute("""CREATE TABLE IF NOT EXISTS users(
                firstN TEXT,
                lastN TEXT,
                osis INTEGER,
                pass TEXT,
                numPost INTEGER,
                numDeleted INTEGER,
                numBest INTEGER
                )"""
                )
    db.commit()
    db.close()

createPosts()

def checkInfo(user, pswd):

    '''This method checks if the user and password combination
    is valid, and returns error msgs based off that check.'''

    db = sqlite3.connect("data/quaf.db")
    c = db.cursor()
    #Looks for the password of the inputted osis num(aka user)
    for i in c.execute("SELECT pass FROM users WHERE osis = ?",(user,)):
         #If user is found and passwords match
        if i[0] == pswd:
            return "Login Successful - Welcome to QUAF+"
         #If passwords don't match
        else:
            db.close()
            return "Incorrect Password - Try again"
    else:
        #If the user doesn't exist in the table
        db.commit()
        db.close()
        return "This ain't it chief"

#testing function
#print(checkInfo(217412923, "bobo"))
#print(checkInfo(217412923, "bobobobo"))
#print(checkInfo(2174123, "bobo"))

def createAccount(user,pswd,passConf,firstN,lastN):

    '''This method checks inputs when creating an acc
    to make sure user didn't mess up anywhere in the process. If everything
    is good, then the account will be created.'''

    db = sqlite3.connect("data/quaf.db")
    c = db.cursor()
    #checks if user is an osis
    if((not isinstance(user, int)) or (len(str(user))!= 9) ):
        return "Not an integer or not the right length for osis"

    #checks if the username already exists
    for i in c.execute("SELECT osis FROM users WHERE osis = ?",(user,)):
        db.close()
        return "Username already exists - Stop trying to steal someone's identity"
    else:
        #if password confirmation fails
        if pswd != passConf:
            db.close()
            return "Passwords do not match - Try again"
        #if password confirmation succeeds add the user to the database
        userdb="INSERT INTO users(osis, pass, firstN, lastN) VALUES( ?, ?, ?, ?)"
        c.execute(userdb,(user,pswd,firstN,lastN))
        db.commit()
        db.close()
        return "Account creation successful"

#testing functions
#print(createAccount(217412923, "bobo", "bobo", "bo", "lu"))
#print(createAccount("217412923", "bo", "bo", "hello", "lu"))
#print(createAccount(2174123, "bobo", "bobo", "bo", "lu"))
#print(createAccount(217412223, "bobo", "bobo", "bo", "lu"))

"""
def findParent(reply):
    db = sqlite3.connect("data/quaf.db")
    c = db.cursor()
    for i in c.execute("SELECT parentID FROM replies WHERE replyID = ?",(reply,)):


def createReply(author, parent, content):

    '''
    This method creates a reply to posts and stores it in the database. It will imitate
    a comment tree similar to that of reddit, and that will be done through searching through
    the potential parent reply.
    '''

    db = sqlite3.connect("data/quaf.db")
    c = db.cursor()

    replyID = random.randint(1,99999999999999999999)
"""
