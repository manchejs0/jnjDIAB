import time
import os
import json
import globalvar
import directMethodSoftwareUpdate
import requests
import sys
import serial
import datetime
import dbFunctions
import iothub_client
import alpha
import subprocess
import logging
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

PROTOCOL = IoTHubTransportProvider.MQTT

logging.basicConfig(filename = '/home/pi/Desktop/project/diabpi.log', level = logging.DEBUG)



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
            
            
            
        else:
            
            globalvar.TELEMETRY_FREQ = 5
            
            

def send_confirmation_callback(message, result, user_context):
    print( "IoT Hub responded to message with status: %s" % (result) )
    
def iothub_client_init():
    client = IoTHubClient(globalvar.CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():
    
    try:
        client = iothub_client_init()
        logging.info( "IoT Hub device sending periodic messages, press Ctrl+C to exit")
        
        client.set_device_method_callback(directMethodSoftwareUpdate.device_method_callback, None)
        client.set_device_twin_callback(device_twin_callback, globalvar.TWIN_CONTEXT)
        
        
        while True:
            
            try: 
                #Start reading values from the pulse sensor and storing it in a SQLite database.
                
                dbFunctions.storeValue()
                
                #Retrieve the most recent value stored in the SQLite database.
                
                
                list = dbFunctions.getValue()
                    
                pulse = list[1]

                timestamp = list[2]
                
                #We have to add strings because otherwise it will cause an error with Thingworx
                
                timestamp1 = "'" + timestamp + "'"
                
                output = subprocess.Popen(['sudo','hologram','modem','signal'], stdout=subprocess.PIPE).communicate()[0]
                
                rightOutput = output.decode("utf-8")
                
                rightOutput.replace(',' , '.')
                
                bad, good = rightOutput.split(":")
                
                better, evenBetter = good.split(",")
                
                best = better+ "." + evenBetter
                
                file = open("location.txt")
                
                location = file.read()
                
                latitude, longitude = location.split(" ")
                
                
                
                
                msg_txt_formatted = globalvar.MSG_TXT % (float(pulse), timestamp1, float(latitude), float(longitude), float(best))
                message = IoTHubMessage(msg_txt_formatted)
                
                logging.info("Sending message : %s" % message.get_string() )
                client.send_event_async(message, send_confirmation_callback, None)
                
                dbFunctions.changeFlag()
                
                time.sleep(int(globalvar.TELEMETRY_FREQ))
                
            except TypeError:
                logging.warning("Type error.")
                pass
            
    except IoTHubError as iothub_error:
        logging.warning( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        logging.info( "IoTHubClient sample stopped")

            
if __name__ == '__main__':
    logging.info( "IoT Hub Quickstart #1 - Simulated Device" )
    logging.info( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
    
