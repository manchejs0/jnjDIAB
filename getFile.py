import requests
from os import getcwd()

url = "https://raw.githubusercontent.com/manchejs0/jnjDIAB/master/webPageConfig.txt"



filename = '/home/pi/AzureFolderwebPageColor.txt'

r = requests.get(url)

thing = str(r.content, 'utf-8')

f = open(filename, 'w')
f.write(thing)

f.close()




