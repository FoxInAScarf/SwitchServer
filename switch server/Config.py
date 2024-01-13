import os

password = ""

def initPassword():

    try:
        open("/etc/password.pwd")

    except:
        os.system("touch /etc/password.pwd")

    global password

    passwordFile = open("/etc/password.pwd", "r", encoding="UTF-8")
    lines = passwordFile.readlines()

    if len(lines) == 0:
        password = ""
    
    else:
        password = lines[0].strip()

    passwordFile.close()

def setPassword(pwd):

    global password
    passwordFile = open("/etc/password.pwd", "w", encoding="UTF-8")
    password = pwd
    passwordFile.write(pwd)
    passwordFile.close()