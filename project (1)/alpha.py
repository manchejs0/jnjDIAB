import usb.core
import usb.util
import os
import subprocess
import time
import logging
import sqlite3

logging.basicConfig(filename = '/home/pi/Desktop/project/diabpi.log', level = logging.DEBUG)

def internetConnection():
    
#Unfortunately, the command to get the location will disconnect the Pi.  Since we're not demoing on a train or plane, just retrieving the location values once should suffice.

    i = 0
    logging.info("Inside alpha.py")

    while True:
        try:
            
            #Looks specifically for the Nova device.
            dev = usb.core.find(idVendor=0x1546, idProduct=0x1102)
            
            #logging.info("Value of dev is " + str(dev))
            logging.info("Inside parent while loop.")
     
            while (i == 0):
                
                global i 

                output = subprocess.Popen(['sudo','hologram','modem','location'], stdout=subprocess.PIPE).communicate()[0]
                
                rightOutput = output.decode("utf-8")
                logging.info("Output of subprocess is" + rightOutput)
        
                #If the modem is able to detect the location, the output will be longer than 25.  Otherwise, we want to try again.
                if (len(rightOutput) < 25):
                    
                    
                    pass
                    logging.info("Location could not be detected. Trying again...")
                        
                else:
                    #We just need to do some formatting to the output like removing the curly braces and some other tasks.
                    newoutput = rightOutput.replace("{","")

                    newnewoutput = newoutput.replace("}","")

                    list = []
                    for token in newnewoutput.split():
                
                        list.append(token)
                
                    longitude = list[6]
                    latitude = list[8]

                    newlongitude = longitude.replace("\"","")
                    newlatitude = latitude.replace("\"","")

                    bestlongitude = newlongitude.strip(',')
                    bestlatitude = newlatitude.strip(',')
                    
                    file = open("location.txt", "w")
                    
                    file.write(bestlatitude + " " + bestlongitude)
                    
                    file.close()
                    
                    logging.info("Location written to file.")
                    
                    #Break this loop.
                    i+=1
            
            if dev is not None:
                #Ping google to make sure internet connection works.
                response = os.system("ping -c 1 " + "google.com")
               
                print(response)
                if (response == 0):
                    #Now, we'll add the signal strength to Sqlite3 as well.
                    logging.info('network connected.')
                    
                    time.sleep(30)
                   
                else:
                    try:
                        os.system('sudo hologram modem disconnect')
                        os.system('sudo hologram modem connect')
                        logging.info('connecting to network')
                        
                    except:
                        pass
                    
            else:
                hologram.network.disconnect()
                logging.info('Device not found.')
                

        except KeyboardInterrupt:
            print("Done.")
            
        except:
            pass
                
if __name__ == '__main__':
    
    internetConnection()
    
