
# coding: utf-8

# ## Import pymongo

# In[1]:


import pymongo


# In[2]:


from pymongo import MongoClient


# ## Connect to database

# In[3]:


client=MongoClient('localhost')
# Could connect to a DB with any arbitrary URI or port number here


# In[4]:


db=client.packt
# This is lazy: packt database doesn't exist yet!


# In[5]:


testCollection=db.testCollection
# This is also lazy: testCollection doesn't exist yet!


# In[8]:


db.drop_collection('testCollection')


# ## Insert some documents

# In[9]:


testCollection.insert_one({'name':'Alice','salary':50000})
testCollection.insert_one({'name':'Bob','salary':40000})
testCollection.insert_one({'name':'Charlie','salary':60000})


# ## Set an Individual Document

# In[11]:


testCollection.update_one({'name':'Alice'},{'$set':{'salary':55000}})


# In[12]:


testCollection.find_one({'name':'Alice'})


# ## Remove a Field from a Document

# In[13]:


testCollection.update_one({'name':"Alice"},{'$unset':{"salary":""}})


# In[14]:


testCollection.find_one({'name':"Alice"})


# ## Calculate total and mean salary

# In[103]:


pipeline=[]


# In[104]:


pipeline.append({"$match":{"salary":{'$exists':"True"}}})


# In[105]:


pipeline.append({'$group':{"_id":None,"avSalary":{"$avg":"$salary"},"totalSalary":{"$sum":"$salary"}}})


# In[106]:


cur=testCollection.aggregate(pipeline=pipeline)


# In[107]:


cur.next()


# ## Calculate total and mean salary over groups

# In[108]:


testCollection.drop()


# In[109]:


testCollection.insert_one({'name':'Alice','salary':50000,'unit':'legal'})
testCollection.insert_one({'name':'Bob','salary':40000,'unit':'marketing'})
testCollection.insert_one({'name':'Charlie','salary':60000,'unit':'communications'})
testCollection.insert_one({'name':'David','salary':70000,'unit':'legal'})
testCollection.insert_one({'name':'Edwina','salary':90000,'unit':'communications'})


# In[113]:


pipeline=[]
pipeline.append({'$group':{"_id":"$unit","avSalary":{"$avg":"$salary"},"totalSalary":{"$sum":"$salary"}}})


# In[114]:


cur=testCollection.aggregate(pipeline=pipeline)


# In[115]:


for d in cur:
    print d

