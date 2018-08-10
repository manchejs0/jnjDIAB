import time
import directMethodSoftwareUpdate
import requests
import sys
import serial
import datetime
import pymongo
import dbFunctions
import getFile
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

#Create a serial connection with the correct protocol

ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=5)

#Global variable -- used for the software upgrade functionality


# Create a client to interact with MongoDB

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database where the appropriate values are located

mydb = myclient["mydatabase"]

# Select the table(collection) where the data is
mycol = mydb["data"]


CONNECTION_STRING = "HostName=jnj-diabpi.azure-devices.net;DeviceId=diabpi;SharedAccessKey=x/O4hgdG8ROelZsCj8lQshKFbDJCw8r0tFHaIkLX/pA="

PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 100000

#Define the JSON message to send to IoT Hub.

MSG_TXT = "{\"pulse\": %.2f, \"time\": %s}"

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
        
        while True:
            #Build message with telemetry values.
            
            mydict = { "pulse": int(ser.readline()), "timestamp":datetime.datetime.now(), "sent": 0}
    
            x = mycol.insert_one(mydict)
            
            dict = dbFunctions.getPulseJson()
    
    
            pulse = dict['pulse']
    
            timestamp = dict['timestamp']
             
            msg_txt_formatted = MSG_TXT % (float(pulse), timestamp)
            message = IoTHubMessage(msg_txt_formatted)
            
            print ("Sending message : %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(10)
            
    except IoTHubError as iothub_error:
        print( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print( "IoTHubClient sample stopped")
            
if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated Device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
