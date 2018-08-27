
# coding: utf-8

# ## Import pymongo

# In[ ]:


import pymongo


# In[ ]:


from pymongo import MongoClient


# ## Connect to database

# In[ ]:


client=MongoClient('localhost')
# Could connect to a DB with any arbitrary URI or port number here


# In[ ]:


db=client.packt
# This is lazy: packt database doesn't exist yet!


# In[ ]:


testCollection=db.testCollection
# This is also lazy: testCollection doesn't exist yet!


# ## Insert some documents

# In[ ]:


import random,string


# In[ ]:


letters=list(string.lowercase)


# In[ ]:


letters[0:5]


# ### Insert many together

# In[ ]:


res=testCollection.insert_many([{random.choice(letters):random.randint(1,10)} for i in range(10)])


# ## Retrieve Documents with a Cursor

# In[ ]:


cur=testCollection.find()


# In[ ]:


type(cur)


# In[ ]:


cur.count()


# In[ ]:


for doc in cur:
    print doc


# In[ ]:


cur.explain()


# ## Good practice to close cursors when finished

# In[44]:


cur.alive


# In[45]:


cur.close()


# In[ ]:


db.testCollection.drop()

