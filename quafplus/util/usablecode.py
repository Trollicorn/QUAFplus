import sqlite3
import datetime

import hashlib

#if local
DB_FILE = "data/quaf.db"
try:
    sqlite3.connect(DB_FILE)
except sqlite3.OperationalError:
#if on virtual machine
    DB_FILE = '/var/www/QUAFplus/QUAFplus/data/quaf.db'

def db_reset():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS posts;")
    c.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT, snips TEXT, author INT, parent INT, tags TEXT, date TEXT, server INTEGER, answered INTEGER, best INTEGER, question INTEGER);")
    c.execute("DROP TABLE IF EXISTS users;")
    c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, firstN TEXT, lastN TEXT, email TEXT, pass TEXT, numPost INTEGER, numDeleted INTEGER, numBest INTEGER);")
    c.execute("DROP TABLE IF EXISTS servers;")
    c.execute("CREATE TABLE servers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, users TEXT, admins TEXT, password TEXT);")
    c.execute("DROP TABLE IF EXISTS nonverified;")
    c.execute("CREATE TABLE nonverified(email TEXT, code TEXT);")
    db.commit()
    db.close()

def class_overview(serverid):
    '''stats for a class'''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT users FROM servers WHERE id = ?;", (serverid,)).fetchone(0)
    lst = []
    for i in b.split(","):
        user = c.execute("SELECT firstN, numPost, numDeleted, numBest FROM users WHERE id=?;",(i,)).fetchone()
        lst.append(({"name": user[0], "numPost": user[1], "numDeleted": user[2], "numBest": user[3]}))
    db.close()
    return lst


def tree(postid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    o = c.execute("SELECT * FROM posts WHERE id=?;", (postid,)).fetchone()
    db.close()
    return{'id': o[0], 'title': o[1], 'body': o[2], 'snips': o[3], 'author': quick_user_inf(o[4]), 'parent': o[5], 'tags': o[6].split(","), 'date': o[7], 'server': o[8], 'answered': True if o[9] == 1 else False, 'best': o[10], 'question': True if o[11] == 1 else False, 'children': [tree(i)for i in get_children(postid)]}


def get_children(parentid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    a = c.execute("SELECT id FROM posts WHERE parent=?;",
                  (parentid,)).fetchall()
    db.close()
    return[i[0]for i in a]


def get_parent(childid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    a = c.execute("SELECT parentid FROM posts WHERE id=?;",
                  (childid,)).fetchone()
    db.close()
    return a[0]


def mk_post(title="", body="", snips="", author=-1, parent=-1, tags="", server=-1, question="false"):
    if server != -1:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("INSERT INTO posts(title, body, snips, author, parent, tags, date, server, answered, best,question) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                  (title, body, snips, int(author), int(parent), tags, str(datetime.datetime.now()), int(server), 0, 0, 1 if question=="true" else 0))
        db.commit()
        db.close()


def rm_post(postid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM posts WHERE id=?;", (postid,))
    db.commit()
    db.close()


def ans_post(postid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE posts SET answered=1 WHERE id=?;", (postid,))
    db.commit()
    db.close()

def edit_post(author, postid, edit):
    '''kind of a basic edit, where only a small note can be adde to the original post'''
    db = sqlite3.connect(DB_FILE)
    c = db. cursor()
    old = str(c.execute("SELECT body FROM posts WHERE id=? AND author=?;", (postid,author,)).fetchone() )
    old += "/n" + edit
    c.execute("UPDATE posts SET body=? WHERE id =?;", (old, postid,))
    db.commit()
    db.close()
    # return old



def quick_user_inf(uid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    u = c.execute("SELECT * FROM users WHERE id = ?;", (uid,)).fetchone()
    db.close()
    return{"first": u[1], "last": u[2], "uid": uid}


def user_profile(uid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    bo = c.execute("SELECT * FROM users WHERE id = ?;", (uid,)).fetchone()
    db.close()
    return{"first": bo[1], "last": bo[2], "email": bo[3], "numPost": bo[5], "numDeleted": bo[6], "numBest": bo[7], "uid": uid}


def home(serverid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    e = c.execute("SELECT * FROM posts WHERE server=? AND parent=-1;",
                  (serverid,)).fetchall()
    db.close()
    return[{'id': o[0], 'title':o[1], 'body':o[2], 'snips':o[3], 'author':quick_user_inf(o[4]), 'parent':o[5], 'tags':o[6].split(","), 'date':o[7], 'server':o[8], 'answered':True if o[9] == 1 else False, 'best':o[10], 'question':True if o[11] == 1 else False}for o in e]


def parents(lowid, child=[]):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    o = c.execute("SELECT * FROM posts WHERE id=?;", (lowid,)).fetchone()
    txt = {'id': o[0], 'title': o[1], 'body': o[2], 'snips': o[3], 'author': quick_user_inf(o[4]), 'parent': o[5], 'tags': o[6].split(
        ","), 'date': o[7], 'server': o[8], 'answered': True if o[9] == 1 else False, 'best': o[10], 'question': True if o[11] == 1 else False, 'children': child}
    db.close()
    return parents(txt['parent'], txt)if-1 != txt['parent']else txt


def user_servers(uid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    servers = c.execute("SELECT id, users FROM SERVERS;").fetchall()
    return[o[0]for o in servers if uid in[int(i)for i in o[1].split(",")]]


def user_servers_dict(uid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    servers = c.execute("SELECT id, users, name FROM SERVERS;").fetchall()
    return[{'id': o[0], 'name':o[2]}for o in servers if uid in[int(i)for i in o[1].split(",")]]

def all_users(serverid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT users FROM servers WHERE id = ?", (serverid,)).fetchone(0)
    list = []
    for i in b.split(","):
        list.append({"name": i})
    return list



def check_admin(uid, serverid):
    if serverid == -1:
        return False
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    o = c.execute("SELECT admins FROM SERVERS where id=?;",
                  (serverid,)).fetchone()
    db.close()
    return str(uid)in o[0].split(",")


def check_user(uid, serverid):
    if serverid == -1:
        return False
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    o = c.execute("SELECT users FROM SERVERS where id=?;",
                  (serverid,)).fetchone()
    db.close()
    return str(uid)in o[0].split(",")


def join_server(uid, serverid):
    if not check_user(uid, serverid):
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        a = c.execute("SELECT users FROM servers where id=?;",
                      (serverid,)).fetchone()[0]+","+str(uid)
        c.execute("UPDATE servers SET users = ? WHERE id=?;", (a, serverid))
        db.commit()
        db.close()


def get_serverName(serverid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT name FROM servers WHERE id=?;", (serverid,)).fetchone()[0]
    return b

def get_serverid(name):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM servers WHERE name=?;", (name,)).fetchone()[0]
    return b


def get_spass(serverid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    a = c.execute("SELECT password FROM servers where id=?;",
                  (serverid,)).fetchone()[0]
    return a


def leave_server(uid, serverid):
    if check_user(uid, serverid):
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        a = c.execute("SELECT users FROM servers WHERE id=?;",
                      (serverid,)).fetchone()[0].split(",")
        a.remove(str(uid))
        c.execute("UPDATE servers SET users = ? WHERE id=?;",
                  (",".join(a), serverid))
        db.commit()
        db.close()


def make_admin(uid, serverid):
    if not check_admin(uid, serverid):
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        a = c.execute("SELECT admins FROM servers where id=?;",
                      (serverid,)).fetchone()[0]+","+str(uid)
        c.execute("UPDATE servers SET admins = ? WHERE id=?;", (a, serverid))
        db.commit()
        db.close()


def remove_admin(uid, serverid):
    if check_admin(uid, serverid):
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        a = c.execute("SELECT admins FROM servers WHERE id=?;",
                      (serverid,)).fetchone()[0].split(",")
        a.remove(str(uid))
        c.execute("UPDATE servers SET admins = ? WHERE id=?;",
                  (",".join(a), serverid))
        db.commit()
        db.close()


def make_server(uid, name, description, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO servers(name,description,users,admins,password) VALUES(?,?,?,?,?);",
              (name, description, str(uid), str(uid), password))
    db.commit()
    db.close()


def user_exists(email):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    tmp = c.execute("SELECT * FROM users WHERE email=?;",
                    (email,)).fetchone() != None
    db.close()
    return tmp


def check_password(email, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    tmp = c.execute("SELECT * FROM users WHERE email=? AND pass=?;",
                    (email, hashlib.md5((email+password).encode("utf-8")).hexdigest())).fetchone() != None
    db.close()
    return tmp


def get_uid(email):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    tmp = c.execute("SELECT * FROM users WHERE email=?;",
                    (email,)).fetchone()[0]
    db.close()
    return tmp


def add_nonverified(email, code):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO nonverified(email, code) VALUES(?,?)",
              (email, code,))
    db.commit()
    db.close()
    return "added"


def get_code(email):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    stuff = c.execute(
        'SELECT code FROM nonverified WHERE email = ?', (email,)).fetchone()
    db.close()
    return stuff[0]


def add_verified(email, passhash, firstN, lastN):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userdb = "INSERT INTO users(firstN, lastN, email, pass, numPost, numDeleted, numPost) VALUES(?, ?, ?, ?, ?, ?, ?)"
    c.execute(userdb, (firstN, lastN, email, passhash, 0, 0, 0,))
    db.commit()
    db.close()
    return "added"


# add_verified("blu4@stuy.edu", "123", "boho", "lu")
# print(get_uid("blu4@stuy.edu"))
# mk_post("testingg", "body", "bleh", 3, -1, "no tag")

# print(edit_post(3, 1, "sup dude"))


# stat = user_profile(get_uid("blu4@stuy.edu"))
# print(stat['first'])
# print(stat['email'])
