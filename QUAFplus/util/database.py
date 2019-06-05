import sqlite3, random

def createDatabase():

    '''Method to initialize our site's database'''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()

    #authorID may just be set to osis for simplicity
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
                postId INTEGER PRIMARY KEY AUTOINCREMENT,
                postTitle TEXT,
                postContent TEXT,
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
                numBest INTEGER,
                identity TEXT
                )"""
                )

    db.commit()
    db.close()

createDatabase()


'''METHODS RELATING TO ACCOUNT CREATION'''
#-------------------------------------------------ACOUNT CREATION TOP-------------------------------------------------
def checkInfo(user, pswd):

    '''
    This method checks if the user and password combination
    is valid, and returns error msgs based off that check.
    '''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    #Looks for the password of the inputted osis num(aka user)
    for i in c.execute("SELECT pass FROM users WHERE osis = ?",(user,)):
         #If user is found and passwords match
        if i[0] == pswd:
            db.close()
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
# print(checkInfo(217412923, "bobo"))
# print(checkInfo(217412923, "bobobobo"))
# print(checkInfo(2174123, "bobo"))

def createAccount(user,pswd,passConf,firstN,lastN):

    '''
    This method checks inputs when creating an acc
    to make sure user didn't mess up anywhere in the process. If everything
    is good, then the account will be created.
    '''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    #checks if user is an osis
    if((not isinstance(user, int)) or (len(str(user))!= 9) ):
        db.close()
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
        userdb="INSERT INTO users(firstN, lastN, osis, pass, numPost, numDeleted, numPost) VALUES( ?, ?, ?, ?, ?, ?, ?)"
        c.execute(userdb,(firstN,lastN, user,pswd, 0, 0 , 0))
        db.commit()
        db.close()
        return "Account creation successful"

#testing functions
# print(createAccount(217412923, "bobo", "bobo", "bo", "lu"))
# print(createAccount("217412923", "bo", "bo", "hello", "lu"))
# print(createAccount(2174123, "bobo", "bobo", "bo", "lu"))
# print(createAccount(217412223, "bobo", "bobo", "bo", "lu"))
#-------------------------------------------------ACOUNT CREATION BOTTOM-------------------------------------------------


'''METHODS RELATING TO REPLIES'''
#-------------------------------------------------REPLIES TOP-------------------------------------------------
def findParent(reply):

    '''Helper method to return parent(if it exists) of a reply'''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    for i in c.execute("SELECT parentID FROM replies WHERE replyID = ?",(reply,)):
        db.close()
        return i[0]

#print(findParent(226311524667076))


def createReply(author, parent, content):


    '''
    This method creates a reply to posts and stores it in the database. It will imitate
    a comment tree similar to that of reddit, and that will be done through searching through
    the potential parent reply.
    '''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    randomID = random.randint(1,9999999999999999)
    print(randomID)
    #parent exists
    if parent != 0:
        reply="INSERT INTO replies(replyID, replyContent, parentID, authorID) VALUES(?, ?, ?, ?)"
        c.execute(reply,(randomID, content, parent, author))
        db.commit()
        db.close()
        return "reply with parent created"

    #no parent
    else:
        reply="INSERT INTO replies(replyID, replyContent, replyID) VALUES(?, ?, ?)"
        c.execute(reply,(randomID, content, author))
        db.commit()
        db.close()
        return "reply w/o parent created"

def replyContent(replyID):
    '''returns the content of a given reply'''
    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    for i in c.execute("SELECT replyContent FROM replies WHERE replyID = ?", (replyID,)):
        db.close()
        return i[0]



#simulated scenario by commenting out each print in order(THESE REPLY ID'S WILL BE DIFFERENT EACH TIME BC OF RANDOM NUM GENERATION):
#print(createReply(217412924, 0, "I like doggo" )) #no parent. replyID = 3775107346189140 based off print statement
#print(findParent(3775107346189140)) #expected to have no parent - CONFIRMED
#print(createReply(217412923, 3775107346189140, "I like doggo 2" )) #with parent from above, replyID = 1561798482773402
#print(findParent(1561798482773402)) #expected to be replyID from the first print statement - CONFIRMED
#print(createReply(217412923, 1561798482773402, "I like doggo2" )) #parent is the child of the parent from first reply replyID = 8419834655865147
#print(findParent(8419834655865147)) #expected to be 1561798482773402 - CONFIRMED
#print(replyContent(1561798482773402)) #expect I like doggo 2 - CONFIRMED

#-------------------------------------------------REPLIES BOTTOM-------------------------------------------------



'''METHODS RELATING TO POSTS'''
#-------------------------------------------------POSTS TOP----------------------------------------------------

def createPost(title, content, author, tag):

    '''Method to add an user's post into the database'''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()

    post = "INSERT INTO posts(postTitle, postContent, authorID, tags) VALUES(?, ?, ?, ?)"
    c.execute(post,(title, content, author, tag))
    db.commit()
    db.close()

    return "post created"



#-------------------------------------------------POSTS BOTTOM-------------------------------------------------

'''METHODS RELATING TO USER INFO'''
#-------------------------------------------------USER INFO TOP-------------------------------------------------
def sortBy(column):

    '''Method to return the database sorted by the column'''

    '''should work probably hopefully'''

    db = sqlite3.connect("../data/quaf.db",row_factory=sqlite3.Row)
    c = db.cursor()
    thing = c.execute("SELECT * FROM users").fetchall()
    thing.sort(key=lambda x: x[column])
    return thing
