#! /usr/bin/env python3
# Wikiedit
# Create by [[zh:U:Emojiwiki]]

import requests
import os
import getpass
import time
import datetime
S = requests.Session()

username = getpass.getuser()
def chroot():
    url1 = str(input("Please type the place of api.php: [https://zh.wikipedia.org/w] "))
    if url1 == "":  
        url1 = "https://zh.wikipedia.org/w"
    url = url1 + "/api.php"
    urlthumb = url1 + "/thumb.php"

def countlist(l):
    lc = 0
    for b in l:
        lc = lc + 1
    return lc

def token(tokentype,url):
    PARAMS_TOKEN = {
        "action": "query",
        "format": "json",
        "meta": "tokens",
        "type": tokentype
    }
    TOKEN_GET = S.get(url=url,params=PARAMS_TOKEN)
    TOKEN_DATA = TOKEN_GET.json()
    print(TOKEN_DATA)
    TOKEN = TOKEN_DATA['query']['tokens'][tokentype + 'token']
    print("Token get sucess!")
    print("Token: " + TOKEN)
    return TOKEN

def login(url,username,passwd,token):
    PARAMS_log = {
        'action':"login",
        'lgname':username,
        'lgpassword':passwd,
        'lgtoken':token,
        'format':"json"
    }
    R = S.post(url, data=PARAMS_log)
    DATA = R.json()
    if DATA['login']['result'] == 'Success':
        print("Login Success!")
        prevlog = "type: Login\nStatus:Sucess\nDATA:" + str(DATA)
    else:
        print("Login Failed")
        prevlog = "type: Login\nStatus:Failed\nDATA:" + str(DATA)

def edit(url,pagename,token):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    PARAMS_pagecontents = {
        'action':"parse",
        'page':pagename,
        'prop':"wikitext",
        'formatversion':"2",
        'format':"json",
    }
    R = S.get(url,params=PARAMS_pagecontents)
    DATA = R.json()
    prevlog = "type: get page text\nDATA:" + str(DATA)
    pagetmp = open("/tmp/Wikiedit" + username,"w+")
    try:
        pagedata = str(DATA["parse"]["wikitext"])
    except:
        if DATA["error"]["code"] == 'missingtitle':
            pass
    else:
        pagetmp.write(pagedata)
    pagetmp.close()
    os.system("nano /tmp/Wikiedit" + username)
    if str(input("Do you want to write this change to the wiki? ")) == "yes":
        PARAMS_edit = {
            "action": "edit",
            "title": pagename,
            "format": "json",
            "starttimestamp":str(timestamp),
            "text": str(open("/tmp/Wikiedit" + username,"r").read()),
        }
        R = S.post(url,params=PARAMS_edit,data={"token": token,})
        DATA = R.json()

def view(url,pagename):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    PARAMS_pagecontents = {
        'action':"parse",
        'page':pagename,
        'prop':"wikitext",
        'formatversion':"2",
        'format':"json",
    }
    R = S.get(url,params=PARAMS_pagecontents)
    DATA = R.json()
    pagetmp = open("/tmp/Wikiedit" + username,"w+")
    try:
        pagedata = str(DATA["parse"]["wikitext"])
    except:
        if DATA["error"]["code"] == 'missingtitle':
            print("Page not found")
            notfound = 1
    else:
        pagetmp.write(pagedata)
        notfound = 0
    pagetmp.close()
    if notfound == 0:
        os.system("less /tmp/Wikiedit" + username)

def credits():
    print("Wikiedit Version stable 1.5 branch 0")
    print("Author: Emojiwiki")
    print("Licence: CC BY-SA 3.0")

def help():
    print("login : Use your username or botpassword to login")
    print("view  : View a page's source code")
    print("edit  : Edit a page")
    print("exit  : Exit TextWikiEdit")
    print("chroot: Change the target wiki (this will run at startup)")

def getimage(url,img):
    PARAMS_getimage ={
        "f":str(img),
        "w":9999
    }
    newFileByteArray = bytearray(requests.get(url,params=PARAMS_getimage).content)
    newFile = open(str(img), "wb+")
    newFile.write(newFileByteArray)
    
chroot()
print("Wikiedit Version stable 1.5 branch 0")
print("Type \"credits\", \"help\" for more information.")
while True:
    try:
        command = str(input("Wikiedit > ")).split( )
        if command == []:
            placeholder = "hiuygtrewt7"
        elif command[0] == "edit":
            if countlist(command) == 1:
                print("Missing args: Title")
            else:
                edit(url,command[1],token("csrf",url))
        elif command[0] == "login":
            username = str(input("Enter username: "))
            userpasswd = getpass.getpass(prompt="Enter password: ")
            login(url,username,userpasswd,token("login",url))
            userpasswd = "0164393648351932643849"
        elif command[0] == "view":
            if countlist(command) == 1:
                print("Missing args: Title")
            else:
                view(url,command[1])
        elif command[0] == "credits":
            credits()
        elif command[0] == "help":
            help()
        elif command[0] == "getimage":
            if countlist(command) == 1:
                print("Missing args: Image")
            else:
                getimage(urlthumb,command[1])
        elif command[0] == "exit":
            exit(1)
        elif command[0] == "chroot":
            chroot()
        elif command[0] == "reload":
            os.system("/usr/bin/env python3 " +str(__file__));exit(1)
        else:
            print(str(command[0]) + ": Command not found")
    except KeyboardInterrupt:
        print()
        pass
    except EOFError:
        print()
        exit(1)
