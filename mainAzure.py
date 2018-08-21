import time
import json
import globalvar
import directMethodSoftwareUpdate
import requests
import sys
import serial
import datetime
import dbFunctions
import iothub_client

from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue



"""
First, we have to setup some things to be able to send messages to the IoT Hub.

We need a connection string, a protocol, a defined time for messages to timeout, and the message that we will later pass real
values into.

"""


CONNECTION_STRING = "HostName=jnj-diabpi.azure-devices.net;DeviceId=diabpi;SharedAccessKey=uDGCy46qmPRxZHG5dQJ0zlRYVKc4RN5AGyQfc5sIfk0="
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 100000
MSG_TXT = "{\"heartRate\": %.2f, \"timestamp\": %s}"
TWIN_CONTEXT = 0




"""

Now, we get into the main body of the code

"""

def device_twin_callback(update_state, payload, user_context):
    print("")
    print( "Twin callback called with:")
    print( "   updateStatus: %s" % update_state)
    print("    payload: %s" % payload)
    
    json_acceptable_string = payload.replace("'", "\"")
    
    d = json.loads(json_acceptable_string)
    
    try:
        
        
        globalvar.TELEMETRY_FREQ = d["desired"]["telemetryFrequency"]
        
    except:
        
        
        if(int(d["telemetryFrequency"])%5 == 0 and int(d["telemetryFrequency"]) > 0):
            
            globalvar.TELEMETRY_FREQ = d["telemetryFrequency"]
            
        elif(int(d["telemetryFrequency"]) == 0 or int(d["telemetryFrequency"]) < 0):
            
            print("Can't accept negative values.  Frequency defaulted to 10.")
            
            
            
            globalvar.TELEMETRY_FREQ = 10
            
        else:
            
            globalvar.TELEMETRY_FREQ = 10
   
    
    

def send_confirmation_callback(message, result, user_context):
    print( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client



def iothub_client_telemetry_sample_run():
    
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl+C to exit")
        
        client.set_device_method_callback(directMethodSoftwareUpdate.device_method_callback, None)
        client.set_device_twin_callback(device_twin_callback, TWIN_CONTEXT)
        
        while True:
           
            #Start reading values from the pulse sensor and storing it in a SQLite database.
            
            dbFunctions.storeValue()
            
            #Retrieve the most recent value stored in the SQLite database.
            list = dbFunctions.getValue()
            
            
    
            pulse = list[1]

            timestamp = list[2]
            
            #We have to add strings because otherwise it will cause an error with Thingworx
            
            timestamp1 = "'" + timestamp + "'"
	    
            msg_txt_formatted = MSG_TXT % (float(pulse), timestamp1)
            message = IoTHubMessage(msg_txt_formatted)
            
            print ("Sending message : %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(int(globalvar.TELEMETRY_FREQ))
           
            
    except IoTHubError as iothub_error:
        print( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print( "IoTHubClient sample stopped")
            
if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated Device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
