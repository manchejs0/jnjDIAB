import pymongo

def getPulseJson():
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    
    mydb = myclient["mydatabase"]
    
    mycol = mydb["data"]
    
    myquery = {"sent" : 0}
    
    #Filter only unsent, only grab pulse and timestamp fields
    
    for x in mycol.find(myquery, {"sent": 0}):
        value = x
    return value
    
    
def updateSent():
    
    newValue = {"$set": {"sent": 1}}
    
