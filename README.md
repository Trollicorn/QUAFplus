# QUAFplus (self-titled)
[![Build Status](https://travis-ci.com/Trollicorn/QUAFplus.svg?branch=master)](https://travis-ci.com/Trollicorn/QUAFplus)
PM Mohammed Uddin, Bo Lu, Theodore Peters, Simon Tsui

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
- activate virtual environment
- do `pip install -r requirements.txt` to install requireled libraries
- do `python3 QUAFplus/__init__.py`to run the app
- go to 127.0.0.1 to view the app

### Apache2 (install and run on Apache2)
- `cd` into `/var/www/` by running `cd /var/www`
- clone the repository and `cd` into it
- in the `QUAFplus.conf` file, change the *ServerName* to where users will go to use the app
- do `chgrp -R www-data QUAFplus` and `chmod -R g+w QUAFplus` to give the app permission to do stuff
- move the `QUAFplus.conf` file into the apache config by doing `mv QUAFplus.conf ../../../etc/apache2/sites-available`
- go to the *sites-available* directory and do `a2ensite QUAFplus`
- do `service apache2 reload`
- go to whatever place you put in *ServerName* in the `QUAFplus.conf` file to view the app
- follow [these instructions](https://docs.google.com/document/d/12b4gf9_1EiJDt6ValtoDVsZPLhGhyOdmnW4n2Xg5E-A/edit)
 if you still need help
