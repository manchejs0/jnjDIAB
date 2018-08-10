# jnjDIAB


This is the repository for the code necessary to run DIABLO.

The main script is mainAzure.py.  This script contains the code that allows the device to send telemetry data to the IoT Hub.

It interacts with a couple of other scripts.  The dbFunctions script retrieves the pulse values stored in the mongoDB database.  

The FileUpload script contains the function required to invoke a direct method to implement a software upgrade.  The code retrieves a file from GitHub, downloads the contents of that file, and writes it to a specified location on the Pi.  The globalvar.py file is necessary to implement this functionality, as it stores the global "softwareVersion" variable that is required to understand the logic for the software upgrade.

