from os import urandom
with open("secret.txt","wb") as f:
    f.write(urandom(32))
