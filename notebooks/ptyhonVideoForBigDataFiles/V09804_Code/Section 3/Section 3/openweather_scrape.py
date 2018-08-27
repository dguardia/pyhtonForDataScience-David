
# coding: utf-8


import requests,pprint,json,time
from pymongo import MongoClient
from secrets import *



def getData(city):
    requestString=u'https://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s' % (city,key)
    
    res=requests.get(requestString)
    
    return res



client=MongoClient('localhost')
db=client.packt


weatherCollection=db.weather


# ## Get lsit of cities

with open('data/city.list.json','r') as inFile:
    citiesJson=json.loads(inFile.read())


citiesJsonCL=filter(lambda x:x[u'country']==u'CL',citiesJson)



cities=map(lambda x:x['name'],citiesJsonCL)
ids=map(lambda x:x['id'],citiesJsonCL)


# ## Cycle through cities


for i,name in zip(ids,cities):
    
    res=getData(name)
    
    if not res.status_code==200:
        print 'Error grabbing data for %s' % name
        print res.reason
        
    else:
        try:
            weatherCollection.insert_one(res.json())
        except e:
            print 'Error inserting into DB' % e
            print '(City %s)' % name
    
    time.sleep(1)
