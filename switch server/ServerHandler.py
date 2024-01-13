import socket
import time
import serial
import glob

running = False

connection = socket.socket()
ipAddress = "10.0.0.2"

arduino = None

def powerOn():

    print("Waking up server...")

    global running
    running = True

    arduino.write("wakeup\n".encode())
    time.sleep(60)
    connection.connect((ipAddress, 40600))

    print("Server has started up!")

def powerOff():
    
    print("Shutting down server...")

    global running
    running = False

    connection.send("shutdown".encode())
    connection.close()
    time.sleep(20)

    print("Server has shut down!")

def restart():
    
    print("Restarting...")

    powerOff()
    powerOn()

def initArduino():

    global arduino

    print("Searching for arduino...")
    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")

    print(ports)

    for port in ports:

        try:

            ser = serial.Serial(port=port, baudrate=9600, timeout=2)
            time.sleep(2)

            ser.write("status\n".encode())
            response = ser.readline().decode().strip()

            time.sleep(1)
            ser.close()

            if response == "arduino4060":

                print("Arduino found!")
                arduino = serial.Serial(port=port, baudrate=9600)
                time.sleep(2)
                return
        
        except:
            pass

    print("Arduino not found! Terminating...")
    exit(1)