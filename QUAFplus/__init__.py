import datetime

from flask import Flask, render_template, url_for, redirect, send_from_directory, request,flash,Request,session,make_response
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
import string, random
try:
    from QUAFplus import pp as pp
except ModuleNotFoundError:
    import pp
from util import usablecode as database

#from util import database

app = Flask(__name__)

DIR = "/var/www/QUAFplus/QUAFplus/"
#mail stuff
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  #using SSL, do 587 for TLS
app.config['MAIL_USERNAME'] = pp.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = pp.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = pp.MAIL_USERNAME
mail = Mail(app)

@app.route('/', methods = ["POST", "GET"])
def main():
    if"userid"not in session:
        return redirect("/login")
    uid=int(session["userid"])
    if request.method=="POST":
        server=request.form["server"]if"server"in request.form else -1
        post=request.form["post"]if"post"in request.form else -1
    else:
        server=request.args["server"]if"server"in request.args else -1
        post=request.args["post"]if"post"in request.args else -1
    return render_template("home.html",server=server,tree=(database.home(server)if post==-1 else database.tree(postid))if server!=-1 and database.check_user(uid,server) else [],is_admin=database.check_admin(),user_id=session["userid"],view_mode="home"if-1==post else"replies",server_list=database.user_servers_dict(uid))

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        formkeys = request.form.keys()
        if not ('email' in formkeys and
                'pass' in formkeys
                ):
            flash("Fill out all fields")
            return render_template('login.html')
        pw = request.form['pass'].strip()
        email = request.form['email'].replace(' ','')
        if not user_exists(email):
            flash("User does not exist with that email")
            return render_template("login.html")
        if not database.check_password(email,pw):
            flash('invalid credentials')
            return render_template('login.html')
        id = database.get_id(email)
        session['userid'] = id
        return redirect('/')

@app.route("/logout")
def logout():
    if'userid'in session:
        session.pop("userid")
    return redirect("/")

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=="GET":
        return render_template("signup.html")
    '''
    should be passed email, first name, and last name
    registers the user
    '''
    formkeys = request.form.keys()
    if not ('email' in formkeys):
        flash("Fill out all fields")
        return render_template('signup.html')
    email = request.form['email'].replace(' ','')
    at = email.find('@')
    if at != -1:
        domain = email[at:]
    if at == -1 or domain != '@stuy.edu': #not valid stuy.edu
        flash('enter valid @stuy.edu address')
        return render_template('signup.html')
    msg = Message('QUAF+ Verification',recipients = [email])
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(6))
    msg.body = 'Your QUAF+ verification code is' + code + '. Go back to the site and go to the /verify route to verify your account.\n\n If you recieved this message in error, please ignore/delete this email.'
    database.add_nonverified(email,fName,lName,code)
    mail.send(msg)
    flash('A verification code has been sent to your email')
    return render_template('verification.html')

@app.route('/verify',methods=["POST","GET"])
def verify():
    formkeys = request.form.keys()
    if not ('email' in formkeys and
            'pass' in formkeys and
            'passConf' in formkeys and
            'code' in formkeys and
            'firstN' in formkeys and
            'lastN' in formkeys
            ):
        flash("Fill out all fields")
        return render_template('signup.html')
    pw = request.form['pass'].strip()
    pwc = request.form['passConf'].strip()
    email = request.form['email'].replace(' ','')
    code = request.form['code'].strip()
    firstN = request.form['firstN'].strip()
    lastN = request.form['lastN'].strip()
    if user_exists(email):
        flash('already verified')
        return render_template('verification.html')
    if pw != pwc:
        flash("passwords don't match")
        return render_template('verification.html')
    activation = database.get_code(email)
    if code != activation:
        flash("activation code does not match")
        return render_template('verification.html')
    passmail = email + pw
    passhash = sha256_crypt.hash(passmail)
    database.add_verified(email,passhash,firstN,lastN)
    return render_template('login.html')

@app.route('/create',methods=["POST","GET"])
def ok():
    if request.method=="POST":
        parent=request.form["parent"]if"parent"in request.form else -1
        server=request.form["server"]if"server"in request.form else -1
    else:
        parent=request.args["parent"]if"parent"in request.args else -1
        server=request.args["server"]if"server"in request.args else -1
    if(server==-1):
        return redirect("/")
    return render_template("create.html",parent=parent,server=server,tree=database.parents(parent)if parent!=-1 else [],is_admin=database.check_admin(),user_id=session["userid"],view_mode="create",server_list=database.user_servers_dict(uid))

#ImmutableMultiDict([('title', ''), ('body', ''), ('snips', '{%{{{{py\r\n\r\n}}}}%}'), ('parent', '-1'), ('server', '-1')])
@app.route('/make_post',methods=["POST"])
def okok():
    if"userid" in session:
        uid=int(session["userid"])
        serverid=int(request.form["server"])
        if database.check_user(uid,serverid):
            database.mk_post(**request.form["title"],author=session["userid"])
    return redirect("/")
@app.route("/delete_post",methods=["POST"])
def okokok():
    if"userid"in session:
        uid=int(session["userid"])
        postid=int(request.form["post"])
        postinfo=database.tree(postid)
        serverid=postinfo["server"]
        if database.check_admin(uid,serverid)or uid==postinfo["author"]["uid"]:
            database.rm_post(postid)
    return redirect("/")
@app.route("/mark_answered",methods=["POST"])
def okokokok():
    if"userid"in session:
        uid=int(session["userid"])
        postid=int(request.form["post"])
        postinfo=database.tree(postid)
        serverid=postinfo["server"]
        if database.check_admin(uid,serverid)or uid==postinfo["author"]["uid"]:
            database.ans_post(postid)
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
