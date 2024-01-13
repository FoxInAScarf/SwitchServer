import socket
import os

alive = True

server = socket.socket()
server.bind(("0.0.0.0", 40600))

server.listen(5)

while alive:
    
    connection, address = server.accept()

    while True:

        try:
            
            request = connection.recv(1024).decode()
            if not request:
                break

            if request == "shutdown":

                alive = False
                break

        except:
            break

    connection.close()
    
server.close()

os.system("shutdown now -h")