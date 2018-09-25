import sqlite3
import datetime
import serial
import time
import globalvar

#Connect to the SQLite database and create a cursor.

conn = sqlite3.connect('/home/pi/Desktop/project/mydb.db')

c = conn.cursor()


#Returns the last value from the database to the mainAzure script.

def getValue():
    
    global c
    
    for row in c.execute('SELECT * from data WHERE sent = 0 ORDER BY id DESC LIMIT 1'):
        
        value = row
        
        
        
        return value
    
 
#Changes the flag field in the database, which indicates whether the message was sent or not.
    
def changeFlag():
    
    global c
    
    for row in ('SELECT * from data ORDER BY id DESC LIMIT 1'):
    
        c.execute('UPDATE data SET sent = 1 WHERE sent = 0 ORDER BY id DESC LIMIT 1')
        
    conn.commit()


def storeValue():
    
    global c
    
    #Setup the serial USB connection
    
    ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=5)
    
    
    
    
    
    latitude = c.execute('SELECT latitude FROM location LIMIT 1').fetchone()
    
    bestLatitude = latitude[0]
    
    
    
    longitude = c.execute('SELECT longitude FROM location LIMIT 1').fetchone()
    bestLongitude = longitude[0]
    
    file = open("/home/pi/Desktop/project/valueCounter.txt")
    
    valueCounter = file.read()
    
    
    
    
    file.close()
    
    try:
        c.execute('INSERT INTO data VALUES(?,?,?,?,?,?)', (valueCounter, float(ser.readline()), str(datetime.datetime.now()), 0, bestLatitude, bestLongitude))
    
        conn.commit()
        
        file = open("/home/pi/Desktop/project/valueCounter.txt", "w")
        
        valueCounter = int(valueCounter) + 1
        
        file.write(valueConter)
        
        file.close()
        
    except:
        pass
    
    
    
        
    
    
    
    
    

    
        



    
    

    
    
    
    
    


    