import pymongo
import sqlite3
import datetime
import serial
import time


conn = sqlite3.connect('mydb.db')

c = conn.cursor()



def getValue():
    
    global c
    
    for row in c.execute('SELECT * from data ORDER BY id DESC LIMIT 1'):
        
        value = row
        return value


def storeValue():
    
    global c
    
    #Setup the serial USB connection
    
    ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=5)
    
    timestamp = str(datetime.datetime.now())
    
    #Make a list of the values we want to send. We want the seconds since epoch so we can order the values easily.
    #Then, we want the pulse, a timestamp to be forwarded to the cloud, and the 'flag' field that determines if the data was sent or not.
    
    
    
    try:
        
        list = [time.time(), float(ser.readline()), timestamp, 0]
    
        c.execute('INSERT INTO data VALUES(?,?,?,?)', (list[0],list[1],list[2],list[3]))
        
        conn.commit()
        
    except ValueError:
        
        pass
    
