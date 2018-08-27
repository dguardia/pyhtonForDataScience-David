
import pymongo, requests, pprint, json, datetime, time
from pymongo import MongoClient
from secrets import *  #saved secret from weather api website (strings)


client=pymongo.MongoClient('pythonforbigdata_this_mongo_1')

db=client.weatherExample  #database called packt
weatherCollection=db.weather  # a collection called weather within weathExample database


#fuction to get multiple cities
def getData(city):
    requestString = 'https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(city, key)
    res = requests.get(requestString)
    return res


# ## Get lsit of cities

with open('city.list.json', 'r') as inFile:
    citiesJson = json.loads(inFile.read())


#creates a python object that is a filter(pointer object) on whole citiesJson python object conserving memory
citiesJsonCL = list(filter(lambda x:x[u'country']==u'CL', citiesJson))

#extract just single item that is easier to pass in list map is another type of python pointer
cities = list(map(lambda x:x['name'],citiesJsonCL))
ids = list(map(lambda x:x['id'], citiesJsonCL))

## cycle through the two lists grab the data for city and insert into mongo db

for i, name in zip(ids, cities):
    
    res = getData(str(name))
    
    if not res.status_code==200:
        print('Error grabbing data for {}, reason {}'.format(name, res.reason))
        #print(res.reason)
    
    else:
        try:
              weatherCollection.insert_one(res.json())
        except e:
              print('Error inserting to DB'.format(e))
              print('City {}'.format(name))
              
    time.sleep(1)