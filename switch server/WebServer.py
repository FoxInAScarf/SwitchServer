from http.cookies import *
import random
import threading
import time

import ZHTTPRequestHandler
import Config
import ServerHandler

sessions = []

class WebServer(ZHTTPRequestHandler.ZHTTPRequestHandler):

    def do_GET(self):

        session = self.getSessionFromCookie()

        # if is authenticated
        if session in sessions:

            self.sendFile("./website/controlPanel.html", 200)
            return

        self.sendFile("./website/login.html", 200)

    def do_POST(self):

        body = self.getPostBody()
        session = self.getSessionFromCookie()

        if self.path == "/login":

            if session in sessions:

                self.sendResponseCode(403)
                return
            
            if body == Config.password:

                session = generateSession(15)
                sessions.append(session)

                self.sendText(session, 200)
                return

            self.sendResponseCode(401)
            return

        # ----------        ONLY FOR AUTHENTICATED USERS        ----------

        if not session in sessions:

            self.sendResponseCode(401)
            return

        if self.path == "/logout":

            sessions.remove(session)
            self.sendResponseCode(200)
            return

        if self.path == "/changePassword":

            Config.setPassword(body)
            self.sendResponseCode(200)
            return

        if self.path == "/toggle":

            thread = None
            if ServerHandler.running:
                thread = threading.Thread(target=ServerHandler.powerOff)

            else:
                thread = threading.Thread(target=ServerHandler.powerOn)

            thread.start()
            time.sleep(1)

            self.sendResponseCode(200)
            return
        
        if self.path == "/restart":

            thread = threading.Thread(target=ServerHandler.restart)
            thread.start()

            self.sendResponseCode(200)
            return

        if self.path == "/status":

            self.sendText(("on" if ServerHandler.running else "off") + "-!&!-" + Config.password, 200)
            return
        
        self.sendResponseCode(400)


    def getSessionFromCookie(self):

        cookies = SimpleCookie(self.headers["Cookie"])
        if "SessionID" in cookies:
            return cookies["SessionID"].value
        
        return None
    
def generateSession(length):

    abc = "abcdefghijklmnopqrstuvwxyz"
    abcUpper = abc.upper()
    nums = "0123456789"

    charset = abc + abcUpper + nums

    session = ""
    for i in range(0, length):
        session += random.choice(charset)

    return session