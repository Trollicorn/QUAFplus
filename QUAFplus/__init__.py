import datetime

from flask import Flask, render_template, url_for, redirect, send_from_directory, request
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt

try:
    from QUAFplus import pp as pp
except ModuleNotFoundError:
    import pp

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

mail = Mail(app)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/authenticate', methods = ["POST", "GET"])
def authenticate():
    """
    status = ''

    if request.method == "GET" or "user" not in request.form.keys():
        return redirect('/')

    if "passConf" in request.form.keys():
        print("\n ACC CREATION \n")
        status = database.createAccount(request.form["user"]. request.form["pswd"], request.form["passConf"], request.form["firstN"], request.form["lastN"])

    else:
        print("\n INFO CONFIRMATION \n")
        status = database.checkInfo(request.form["user"], request.form["pswd"])
    """
    return render_template("signup.html")

@app.route('/create',methods=["POST","GET"])
def ok():
    if request.method=="POST":
        parent=request.form["parent"]if"parent"in request.form else 0
        server=request.form["server"]if"server"in request.form else 0
    else:
        parent=request.args["parent"]if"parent"in request.args else 0
        server=request.args["server"]if"server"in request.args else 0
    return render_template("create.html",parent=parent,server=server)
@app.route('/make_post',methods=["POST"])
def okok():
    print(request.form)
    return redirect('/')
    

if __name__ == "__main__":
    app.debug = True
    app.run()
