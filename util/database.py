import sqlite3

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


def checkInfo(user, pswd):

    '''This method checks if the user and password combination
    is valid, and returns error msgs based off that check.'''

    db = sqlite3.connect("data/quaf.db")
    c = db.cursor()
    #Looks for the password of the inputted osis num(aka user)
    for i in c.execute("SELECT pass FROM users WHERE osis = ?",(user,)):
         #If user is found and passwords match
        if i[0] == pswd:
            return "Login Successful - Welcome to QUAF+!"
         #If passwords don't match
        else:
            db.close()
            return "Incorrect Password - Try again."
    else:
        #If the user doesn't exist in the table
        db.commit()
        db.close()
        return "This ain't it chief."

def createAccount(user,pswd,passConf,firstN,lastN):

    '''This method checks inputs when creating an acc
    to make sure user didn't mess up anywhere in the process. If everything
    is good, then the account will be created.'''

    db = sqlite3.connect("data/quaf.db")
    c = db.cursor()
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
        return "Account creation successful."
