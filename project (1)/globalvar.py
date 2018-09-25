import mainAzure
import alpha


CONNECTION_STRING = "HostName=mdc-poc-iotbub1.azure-devices.net;DeviceId=diabpi;SharedAccessKey=RFKmzlOMEit5UvAuhCGKJtlBv511CNN3XHTFUhjW64o="


TELEMETRY_FREQ = 15



MESSAGE_TIMEOUT = 100000
MSG_TXT = "{\"heartRate\": %.2f, \"timestamp\": %s, \"latitude\": %.2f, \"longitude\": %.2f, \"signalStrength\": %.2f}"
TWIN_CONTEXT = 0


#Log file upload variables

PATHTOFILE = "/home/pi/Desktop/helloWorld.txt"
    
FILENAME = "helloWorld"
    
f = open(PATHTOFILE, "r")
    
content = f.read()

sendLog = True


valueCounter = 1

softwareVersion = 1






