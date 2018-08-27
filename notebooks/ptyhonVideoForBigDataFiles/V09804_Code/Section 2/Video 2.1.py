
# coding: utf-8

# In[27]:


get_ipython().magic(u'load_ext watermark')


# ## Import pymongo

# In[28]:


import pymongo


# In[29]:


get_ipython().magic(u'watermark -p pymongo')


# In[30]:


from pymongo import MongoClient


# ## Connect to database

# In[44]:


client=MongoClient('localhost')
# Could connect to a DB with any arbitrary URI or port number here


# In[45]:


db=client.packt
# This is lazy: packt database doesn't exist yet!


# In[46]:


testCollection=db.testCollection
# This is also lazy: testCollection doesn't exist yet!


# ## Insert and Retrieve Document

# In[47]:


testCollection.insert_one({'a':1})


# In[48]:


testCollection.find_one()


# In[49]:


testCollection.count()


# ## Find a matching document

# In[37]:


res=testCollection.insert_one({'b':2})


# In[38]:


testCollection.find_one({'b':2})


# In[39]:


testCollection.find_one({'b':2},{'_id':0})


# ## Drop a collection and database

# In[40]:


db.drop_collection('testCollection')


# In[41]:


db.drop_collection('testCollection')


# In[43]:


client.drop_database('packt')

