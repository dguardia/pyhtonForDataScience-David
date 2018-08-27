
# coding: utf-8

# In[ ]:


import pandas as pd
import json,pprint


# ## Tabular Data

# In[ ]:


get_ipython().system(u'wget https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data ')


# In[ ]:


df = pd.read_csv('data/iris.data.txt',header=None)


# In[ ]:


df.head()


# ## JSON Data

# In[7]:


with open('data/single_tweet.json','r') as inFile:
    tweet=json.loads(inFile.read())


# In[9]:


tweet.keys()


# In[11]:


tweet['source']


# In[ ]:


pp = pprint.PrettyPrinter(indent=4)


# In[ ]:


pp.pprint(tweet)


# In[ ]:


with open('data/single_tweet.json','w') as outFile:
    outFile.write(s.AsJsonString())


# Follow [steps](https://github.com/bear/python-twitter) to get Twitter API credentials

# In[ ]:


api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)


# In[ ]:


statuses = api.GetUserTimeline(screen_name='arutherfordium')


# In[ ]:


s=statuses[3]

