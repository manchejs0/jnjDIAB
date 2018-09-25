'use strict';

var sent = 0;



	var fs = require('fs');
	var mqtt = require('azure-iot-device-mqtt').Mqtt;
	var clientFromConnectionString = require('azure-iot-device-mqtt').clientFromConnectionString;
	
	var connectionString = 'HostName=mdc-poc-iotbub1.azure-devices.net;DeviceId=diabpi;SharedAccessKey=RFKmzlOMEit5UvAuhCGKJtlBv511CNN3XHTFUhjW64o=';
	var filename = 'helloWorld.txt';
	
	
	var client = clientFromConnectionString(connectionString);
	console.log('Client connected');
	
	
	
		fs.stat(filename, function (err, stats) {
		    const rr = fs.createReadStream(filename);
		
		    client.uploadToBlob("logs/"+filename, rr, stats.size, function (err) {
		        if (err) {
		            console.error('Error uploading file: ' + err.toString());
		        } else {
		            console.log('File uploaded');
			   
			    
		        }
		    });
	});


