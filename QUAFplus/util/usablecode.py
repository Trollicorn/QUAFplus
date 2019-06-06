import sqlite3
import datetime

db = sqlite3.connect("../data/quaf.db")
c = db.cursor()
                     
def db_reset():
    c.execute("DROP TABLE IF EXISTS posts;")
    c.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT, snips TEXT, author INT, parent INT, tags TEXT, date TEXT, server INTEGER, answered INTEGER, best INTEGER, question INTEGER);");
    db.commit()
def tree(postid):
    o=c.execute("SELECT * FROM posts WHERE id=?;",(postid,)).fetchone()
    return{'id':o[0],'title':o[1],'body':o[2],'snips':o[3],'author':quick_user_inf(o[4]),'parent':o[5],'tags':o[6].split(","),'date':o[7],'server':o[8], 'answered':True if o[9]==1 else False, 'best':o[10],'question':True if o[11]==1 else False,'children':[tree(i)for i in get_children(postid)]}
def get_children(parentid):
    a=c.execute("SELECT id FROM posts WHERE parent=?;",(parentid,)).fetchall()
    return[i[0]for i in a]
def get_parent(childid):
    a=c.execute("SELECT parentid FROM posts WHERE id=?;",(childid,)).fetchone()
    return a[0]
def mk_post(title="",body="",snips="",author=-1,parent=-1,tags="",server=-1):
    if server!=-1:
        c.execute("INSERT INTO posts(title, body, snips, author, parent, tags, date, server, answered, best) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",(title,body,snips,author,parent,tags,str(datetime.datetime.now()),server))
        db.commit()
def quick_user_inf(uid):
    u=c.execute("SELECT * FROM users WHERE userid = ?;",(uid,)).fetchone()
    return{"first":u[1],"last":u[2],"numpost":u[5],"numbest":u[7],"uid":uid}
def home(serverid):
    e=c.execute("SELECT * FROM posts WHERE server=?;",(serverid,)).fetchall()
    return[{'id':o[0],'title':o[1],'body':o[2],'snips':o[3],'author':quick_user_inf(o[4]),'parent':o[5],'tags':o[6].split(","),'date':o[7],'server':o[8], 'answered':True if o[9]==1 else False, 'best':o[10],'question':True if o[11]==1 else False}for o in e]
def parents(lowid,child=[]):
    o=c.execute("SELECT * FROM posts WHERE id=?;",(postid,)).fetchone()
    txt={'id':o[0],'title':o[1],'body':o[2],'snips':o[3],'author':quick_user_inf(o[4]),'parent':o[5],'tags':o[6].split(","),'date':o[7],'server':o[8], 'answered':True if o[9]==1 else False, 'best':o[10],'question':True if o[11]==1 else False,'children':child}
    return parents(txt['parent'],txt)if-1!=txt['parent']else txt
