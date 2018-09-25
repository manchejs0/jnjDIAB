import configparser
import os


def get_config():
    
    config = configparser.ConfigParser()
    config.read("/home/pi/Desktop/project/config.ini")
    
    return config


def get_setting(section, setting):
    
    config = get_config()
    
    value = config.get(section, setting)
    
    return value

def update_setting(section, setting, value):
    
    config = get_config()
    
    config.set(section,setting,value)
    
    with open("/home/pi/Desktop/project/config.ini", "wb") as config_file:
        config.write(config_file)
        
        


