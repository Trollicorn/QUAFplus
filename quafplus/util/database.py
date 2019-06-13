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
                tags TEXT,
                postDate TEXT
                )"""
                )

    c.execute("""CREATE TABLE IF NOT EXISTS replies(
                replyID INTEGER,
                replyContent TEXT,
                parentID INTEGER,
                authorID INTEGER
                )"""
                )

    c.execute('''CREATE TABLE IF NOT EXISTS nonverified(
                email TEXT,
                code TEXT
    )'''
    )

    c.execute("""CREATE TABLE IF NOT EXISTS users(
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                firstN TEXT,
                lastN TEXT,
                email TEXT,
                pass TEXT,
                numPost INTEGER,
                numDeleted INTEGER,
                numBest INTEGER
                )"""
                )

    db.commit()
    db.close()

createDatabase()


'''METHODS RELATING TO ACCOUNT CREATION & USERS'''
#-------------------------------------------------ACOUNT CREATION & USERS TOP-------------------------------------------------
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

def createAccount(email,pw,firstN,lastN):

    '''
    This method adds a user to the database
    '''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()

    #checks if the email already exists
    #implement

    userdb="INSERT INTO users(firstN, lastN, email, pass, numPost, numDeleted, numPost) VALUES(?, ?, ?, ?, ?, ?, ?)"
    c.execute(userdb,(firstN,lastN, email, pw, 0, 0 , 0)
    db.commit()
    db.close()
    return "Account creation successful"

def addNonverified(email,firstN,lastN,code):
    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    c.execute("INSERT INTO nonverified(email, firstN, lastN, code) VALUES(?,?,?,?)",(email,firstN,lastN,code,))
    db.commit()
    db.close()
    return "added"

def getCode(email):
    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    stuff = c.execute('SELECT code FROM nonverified WHERE email = ?',(email,)).fetchone()
    db.close()
    return stuff[0]

def addVerified(email,passhash,firstN,lastN):
    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    userdb="INSERT INTO users(firstN, lastN, email, pass, numPost, numDeleted, numPost) VALUES(?, ?, ?, ?, ?, ?, ?)"
    c.execute(userdb,(firstN,lastN,email,passhash,0,0,0,))
    db.commit()
    db.close()
    return "added"


def activateAccount(email,activation):
    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    for i in c.execute("SELECT email FROM users WHERE email = ?",(email,)):
        db.close()
        return "Already verified"
    a = c.execute("SELECT email,pw FROM nonverified WHERE email = ? AND code = ?",(email,activation))
    ## do later


#testing functions
# print(createAccount(217412923, "bobo", "bobo", "bo", "lu"))
# print(createAccount("217412923", "bo", "bo", "hello", "lu"))
# print(createAccount(2174123, "bobo", "bobo", "bo", "lu"))
# print(createAccount(217412223, "bobo", "bobo", "bo", "lu"))
# print(createAccount(12345678, "simon", "simon", "bo", "lu", "student", "I am a very smart dood")) #correctly provides an error
# print(createAccount(None, "brown", "brown", "bo", "lu", "teacher", "I am a very smart dood")) #does not have an error bc its a teacher

def sortBy(column):

    '''Method to return the database sorted by the column'''

    '''should work probably hopefully'''

    db = sqlite3.connect("../data/quaf.db",row_factory=sqlite3.Row)
    c = db.cursor()
    thing = c.execute("SELECT * FROM users").fetchall()
    thing.sort(key=lambda x: x[column])
    return thing
#-------------------------------------------------ACOUNT CREATION & USER BOTTOM-------------------------------------------------


'''METHODS RELATING TO REPLIES'''
#-------------------------------------------------REPLIES TOP-------------------------------------------------
def check_Parent(reply):

    '''Helper method to return parent(if it exists) of a reply'''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    for i in c.execute("SELECT parentID FROM replies WHERE replyID = ?",(reply,)):
        db.close()
        return i[0]

#print(checkParent(226311524667076))


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

def check_replyContent(replyID):
    '''returns the content of a given reply'''
    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()
    for i in c.execute("SELECT replyContent FROM replies WHERE replyID = ?", (replyID,)):
        db.close()
        return i[0]



#simulated scenario by commenting out each print in order(THESE REPLY ID'S WILL BE DIFFERENT EACH TIME BC OF RANDOM NUM GENERATION):
#print(createReply(217412924, 0, "I like doggo" )) #no parent. replyID = 3775107346189140 based off print statement
#print(check_Parent(3775107346189140)) #expected to have no parent - CONFIRMED
#print(createReply(217412923, 3775107346189140, "I like doggo 2" )) #with parent from above, replyID = 1561798482773402
#print(check_Parent(1561798482773402)) #expected to be replyID from the first print statement - CONFIRMED
#print(createReply(217412923, 1561798482773402, "I like doggo2" )) #parent is the child of the parent from first reply replyID = 8419834655865147
#print(check_Parent(8419834655865147)) #expected to be 1561798482773402 - CONFIRMED
#print(check_replyContent(1561798482773402)) #expect I like doggo 2 - CONFIRMED

#-------------------------------------------------REPLIES BOTTOM-------------------------------------------------



'''METHODS RELATING TO POSTS'''
#-------------------------------------------------POSTS TOP----------------------------------------------------

def createPost(title, content, author, tag, date):

    '''Method to add an user's post into the database'''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()

    post = "INSERT INTO posts(postTitle, postContent, authorID, tags, postDate) VALUES(?, ?, ?, ?, ?)"
    c.execute(post,(title, content, author, tag, date))
    db.commit()
    db.close()

    return "post created"


# print(createPost("Test1", "blehbleh", 217412923, "TESTRUN", "Jun 5, 2019")) #works
# print(createPost("Test1", "blehblehbleh", 217412923, "TESTRUN", "Jun 5, 2019"))
# print(createPost("Test2", "blehbleh", 217412923, "TESTRUN", "Jun 5, 2019"))
# print(createPost("Test1", "blahblah", 123456789, "TESTRUN", "Jun 5, 2019"))
# print(createPost("Test2", "blahblahblah", 123456789, "TESTRUN", "Jun 5, 2019"))

def check_postContent(title, author):

    '''checks the content of a post found using the title of post and the author of the post'''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()

    for i in c.execute("SELECT postContent FROM posts WHERE postTitle = ? AND authorID = ?", (title, author,)):
        db.close()
        return i[0]

def check_postDate(title, author):

    '''checks the date of a post found using the title of post and the author of the post'''

    db = sqlite3.connect("../data/quaf.db")
    c = db.cursor()

    for i in c.execute("SELECT postDate FROM posts WHERE postTitle = ? AND authorID = ?", (title, author,)):
        db.close()
        return i[0]



# print(check_postContent("Test1", 217412923))
# print(check_postContent("Test2", 217412923))
# print(check_postContent("Test1", 123456789))
# print(check_postContent("Test2", 123456789))
# print(check_postDate("Test2", 217412923))
# print(check_postDate("Test1", 123456789))


#-------------------------------------------------POSTS BOTTOM-------------------------------------------------
