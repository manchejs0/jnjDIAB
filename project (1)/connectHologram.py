from Hologram.HologramCloud import HologramCloud
import time



#This is essential.  The device key for a device can be found by visting the Hologram dashboard.
credentials = {'devicekey': '#AbCsHw'}

hologram = HologramCloud(credentials, network='cellular')

    

try:

    
    while True:
        status = hologram.network.getConnectionStatus()
        try:
            
           
                
            if (status == 1):
                
                print("Network connected...")
                time.sleep(30)
                    
            else:
                
                print("Connecting to cellular...")
                hologram.network.connect()
       
        except:
            print("Hmm..encountered an error.  We'll try again.")
            
        
except KeyboardInterrupt:
    print("Exiting demo")
            
        

    

        
