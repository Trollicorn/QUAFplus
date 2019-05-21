from flask import Flask, render_template, url_for, redirect, send_from_directory, request

#from util import database

app = Flask(__name__)

DIR = "/var/www/QUAFplus/QUAFplus/"

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

if __name__ == "__main__":
    app.debug = True
    app.run()
