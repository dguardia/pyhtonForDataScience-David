
# coding: utf-8

# In[2]:


from pyspark.sql import Row
import pyspark


# ## Check Spark context loaded

# In[3]:


sc


# ## Create RDD from Iris data

# In[4]:


rdd=sc.textFile('data/iris.data.txt')


# In[5]:


rdd.first()
# Each element of RDD is a line as a single string


# In[7]:


lines=rdd.map(lambda x:x.split(','))


# In[8]:


lines.first()
# Each lines is now split into tokens


# In[9]:


parsedLines=lines.map(lambda x:Row(sepalLength=float(x[0]),sepalWidth=float(x[1]),petalLength=float(x[2])                      ,petalWidth=float(x[3]),species=x[4]))


# In[10]:


parsedLines.first()
# Each line is now names and parsed as float or string


# In[11]:


parsedLines.first()['species']
# We can refer to each token by name


# In[12]:


del rdd
del lines


# ## Create an Unstructured RDD

# In[23]:


sc.parallelize([Row(test=1),Row(test1='a',test2=11)]).collect()


# ## Turn RDD into DataFrame

# In[13]:


from pyspark.sql.types import StructField,StructType, FloatType,StringType


# In[14]:


schema=StructType([StructField('petalLength',FloatType()),
                   StructField('petalWidth',
                FloatType()),StructField('sepalLength',
                FloatType()),StructField('sepalWidth',
                FloatType()),StructField('species',StringType())])


# In[127]:


df=sqlContext.createDataFrame(parsedLines,schema=schema)


# In[128]:


df.first()


# In[129]:


df.head(4)


# In[120]:


df.schema


# ## Create Dataframe from cities JSON file

# In[146]:


df=spark.read.json('data/city.list.clean.json')


# In[147]:


df.count()


# In[148]:


df.head(3)


# In[149]:


df.columns

