from http.server import *
import socket
import threading
import signal
import time

import WebServer
import Config
import ServerHandler

webserver = None

hostShutdownSignal = 0

def init():

    # initialise password
    print("Reading password...")
    Config.initPassword()
    print("Password: " + Config.password)

    # scan all ports, determine which one is the one with the arduino
    ServerHandler.initArduino()

    # determine if server is running, act accordingly
    print("Checking server availability...")
    if not isAlive():

        print("Couldn't connect to server... Server must either be turned off or 'shutdownd' is not running...")
        print("Attempting to start server...")
        ServerHandler.powerOn()

    else:

        print("Successfully connected to server! Establishing permanent connection with 'shutdownd'...")
        ServerHandler.connection.connect((ServerHandler.ipAddress, 40600))
        ServerHandler.running = True
        print("Connection established!")

    # start webserver
    global webserver

    print("Initialising HTTP server...")
    webserver = HTTPServer(("0.0.0.0", 40601), WebServer.WebServer)
    print("HTTP server is now running!")
    thread = threading.Thread(target=webserver.serve_forever)
    thread.start()

    # detect host shutdown
    signal.signal(signal.SIGTERM, onShutdown)    
    signal.signal(signal.SIGINT, onShutdown)
    signal.signal(signal.SIGQUIT, onShutdown)
    signal.signal(signal.SIGABRT, onShutdown)

    while hostShutdownSignal == 0:
        pass

    # end of process actions
    print("Shutting down...")
    webserver.shutdown()
    ServerHandler.arduino.close()
    ServerHandler.connection.close()
    time.sleep(1)

def isAlive():

    connectionTest = socket.socket()
    try:

        connectionTest.connect((ServerHandler.ipAddress, 40600))
        connectionTest.close()
        return True
    
    except:
        return False

def onShutdown(signum, frame):

    print(str(signum) + " " + str(frame))

    global hostShutdownSignal
    hostShutdownSignal = 1

init() 
exit(0)