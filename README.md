# QUAF+ (self-titled)

#Roles
Mohammed Uddin (Project Manager) 
Bo Lu (Databse, Back-end)
Theodore Peters (Javascript, Front-end, Database, Back-end)
Simon Tsui (Front-end)

[Watch our demo video here](https://youtu.be/CUgisLEqsCg)

## Summary
This is a forum tailored specifically for Stuy CS classes

## Necessary Packages
**passlib** - used for hasing passwords for added security
to install: `pip install passlib`

**flask-mail** - used for emailing users
to install: `pip install flask-mail`
*just do `pip install -r requirements.txt` to download both*

## Launch Instructions

### Localhost (install and run on localhost)
- clone the repository and `cd` into it
- cd into the innter `QUAFplus/directory`
- do `python3 xtra.py` to generate  secret key
- create a copy of the file named `pp.py.example` and call it `pp.py`
- in the `pp.py` file, change the value of `MAIL_USERNAME` to a valid gmail email address that you have access to (this email address will be used to send emails)
- in the `pp.py` file, change the value of `MAIL_PASSWORD` to the password of the gmail address used for `MAIL_USERNAME` (don't worry, the `pp.py` file is not tracked by github, and the only way for someone to see your account credentials would be to open the file itself locally)
- do `cd ..` to cd back to the outer QUAFplus directory
- activate virtual environment
- do `pip3 install -r requirements.txt` to install required libraries
- do `python3 QUAFplus/__init__.py`to run the app
- go to 127.0.0.1 to view the app

### Apache2 (install and run on Apache2)
- `cd` into `/var/www/` by running `cd /var/www`
- clone the repository and `cd` into it by doing `cd QUAFplus`
- cd into the inner QUAFplus directory by doing `cd QUAFplus` again
- do `python3 xtra.py` to generate a secret key
- create a copy of the file named `pp.py.example` and call it `pp.py`
- in the `pp.py` file, change the value of `MAIL_USERNAME` to a valid gmail email address that you have access to (this email address will be used to send emails)
- in the `pp.py` file, change the value of `MAIL_PASSWORD` to the password of the gmail address used for `MAIL_USERNAME` (don't worry, the `pp.py` file is not tracked by github, and the only way for someone to see your account credentials would be to open the file itself locally)
- do `cd ..` to cd back to the outer QUAFplus directory
- do `pip3 install -r requirements.txt` to install required libraries
- in the `QUAFplus.conf` file, change the *ServerName* to where users will go to use the app
- do `chgrp -R www-data QUAFplus` and `chmod -R g+w QUAFplus` to give the app permission to do stuff
- move the `QUAFplus.conf` file into the apache config by doing `mv QUAFplus.conf ../../../etc/apache2/sites-available`
- do `cd ../../../etc/apache2/sites-available` to go to the *sites-available* directory 
` do `a2ensite QUAFplus`
- do `service apache2 reload`
- go to whatever place you put in *ServerName* in the `QUAFplus.conf` file to view the app
- follow [these instructions](https://docs.google.com/document/d/12b4gf9_1EiJDt6ValtoDVsZPLhGhyOdmnW4n2Xg5E-A/edit)
 if you still need help
