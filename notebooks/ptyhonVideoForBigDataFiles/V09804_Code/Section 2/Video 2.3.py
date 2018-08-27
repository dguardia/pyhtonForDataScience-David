
# coding: utf-8

# ## Import pymongo

# In[1]:


import pymongo


# In[2]:


from pymongo import MongoClient


# ## Connect to database

# In[3]:


client=MongoClient('localhost')


# In[4]:


db=client.packt


# In[9]:


coll=db.embedded


# ## Insert a document with nested array

# In[10]:


res=coll.insert_one({'ages' : [30,42,12,19]})


# In[ ]:


res=coll.insert_one({'ages' : [18,27,25,19]})


# ### Match entire array

# In[26]:


coll.find_one({'ages' : [30,42,12,19]},{'_id' : 0})


# ### Match on presence of element in array

# In[27]:


coll.find_one({'ages' : 30},{'_id' : 0})


# ### Match array with conditions on any elements in array

# In[28]:


coll.find_one({'ages' : {'$gt':40,'$lt':20}},{'_id' : 0})


# ### Match array with conditions on any single element of array

# In[29]:


coll.find_one({'ages' : {'$elemMatch' : {'$lt' : 22, '$gt' : 15}}},{'_id' : 0})


# ### Match by array index

# In[30]:


coll.find_one({'ages.1' : 42},{'_id' : 0})


# ### Match by condition on array index

# In[31]:


coll.find_one({'ages.1' : {'$gt':40}},{'_id' : 0})


# ## Insert a document with nested dictionary

# In[22]:


res=coll.insert_one({'personInfo' : {'name' : 'Alice', 'age' : 30}})
res=coll.insert_one({'personInfo' : {'name' : 'Bob', 'age' : 42}})
res=coll.insert_one({'personInfo' : {'name' : 'Charlie', 'age' : 12}})
res=coll.insert_one({'personInfo' : {'name' : 'David', 'age' : 19}})


# ### Match by name

# In[32]:


coll.find_one({'personInfo.name' : 'Alice'},{'_id' : 0})


# ### Match by age

# In[33]:


coll.find_one({'personInfo.age' : {'$gt' : 40}},{'_id' : 0})


# ## Match on multiple conditions

# In[47]:


coll.insert_one({"personInfo":{"name":"Alice","age":32}})


# In[49]:


coll.find_one({'personInfo.name':'Alice','personInfo.age':{'$gt':30}},{'_id':0})

