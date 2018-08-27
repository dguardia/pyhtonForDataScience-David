
# coding: utf-8

# In[1]:


sc


# ## Read Mongo collection into Dataframe

# In[2]:


df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
"mongodb://127.0.0.1/packt.testCollection").load()


# In[3]:


df.count()


# In[4]:


df.collect()


# ## Compare to pyMongo

# In[5]:


import pymongo


# In[6]:


from pymongo.mongo_client import MongoClient


# In[7]:


client=MongoClient('localhost')


# In[8]:


db=client.packt


# In[9]:


cur=db.testCollection.find()


# In[10]:


for c in cur:
    print c


# ## Perform query

# In[11]:


pipeline = "{'$match': {'unit': 'legal'}}"


# In[12]:


df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
"mongodb://127.0.0.1/packt.testCollection").option("pipeline",pipeline).load()


# In[14]:


df.collect()

