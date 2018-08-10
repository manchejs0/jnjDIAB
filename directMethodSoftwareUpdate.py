import requests
import globalvar
from iothub_client import DeviceMethodReturnValue

def device_method_callback(method_name, payload, user_context):
    
    
    
          
    
    device_method_return_value = DeviceMethodReturnValue()
    device_method_return_value.response = "{\"Response\": \"This is the response from the device\" }"
    device_method_return_value.status = 200

    
    
    if (method_name == "softwareUpdate"):
        
        
        if (globalvar.softwareVersion == 1):
            print("Updating software")
            globalvar.softwareVersion = 2
            filename =  '/home/pi/azureFolderwebPageColor.txt'
            r = requests.get("https://raw.githubusercontent.com/manchejs0/jnjDIAB/master/webPageConfig.txt")

            thing = str(r.content, 'utf-8')

            f = open(filename, 'w')
            f.write(thing)

            f.close()
        else:
            globalvar.softwareVersion = 1
            print("Updating software")
            filename = '/home/pi/azureFolderwebPageColor.txt'
            r = requests.get("https://raw.githubusercontent.com/manchejs0/jnjDIAB/master/webPageConfig2.txt")
            
            thing = str(r.content, 'utf-8')
            
            f = open(filename, 'w')
            f.write(thing)
            
            f.close()
            
            
	

    else:
        pass
    
    return device_method_return_value
