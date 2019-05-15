from flask import Flask, render_template, url_for, redirect, send_from_directory

app = Flask(__name__)

DIR = "/var/www/QUAFplus/QUAFplus/"

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
