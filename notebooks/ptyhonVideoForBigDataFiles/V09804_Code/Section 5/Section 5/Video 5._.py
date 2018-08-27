
# coding: utf-8

# In[1]:


sc


# ## Take a look at data (5.2)

# In[103]:


from pymongo import MongoClient
import pprint


# In[100]:


client=MongoClient('localhost')


# In[101]:


db=client.packt


# In[102]:


redditCollection=db.reddit


# In[104]:


pprint.pprint(redditCollection.find_one())


# ## Specify schema

# In[3]:


import pyspark.sql.types


# In[134]:


from pyspark.sql.types import StructField,StructType, FloatType,StringType,IntegerType


# In[106]:


schema=StructType([
                StructField('score',IntegerType()),
                   StructField('created_utc',StringType()),
                  StructField('postLength',IntegerType())])


# ## Read Mongo collection into Dataframe

# In[107]:


pipeline = "[{$project:{'score':1,'created_utc':1,'_id':0,'postLength':{$size:{$split:['$body',' ']}}}}]"


# In[109]:


df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
"mongodb://127.0.0.1/packt.reddit").option("pipeline",pipeline).schema(schema).load()


# In[110]:


get_ipython().magic(u'time df.count()')


# In[111]:


df.printSchema()


# ## Convert UTC timestamp to hour

# In[112]:


from pyspark.sql.functions import udf
import datetime


# In[113]:


getHour=udf(lambda x:datetime.datetime.fromtimestamp(int(x)).hour,IntegerType())


# In[114]:


dfClean=df.withColumn('hour',getHour('created_utc'))


# In[115]:


get_ipython().magic(u'time dfCleanPd=dfClean.toPandas()')
# Convert to pandas dataframe for easy plotting


# In[116]:


dfCleanPd.shape


# ## Look at distribution over hour of day

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[117]:


gg=dfCleanPd.groupby('hour')


# In[118]:


gg.agg(['mean'])['postLength'].plot()
plt.title('Mean Post Length')
gg.agg(['mean'])['ups'].plot()
plt.title('Mean Up Score')


# ## Preparing data for spark.ml (5.3)

# In[137]:


from pyspark.ml.feature import VectorAssembler
# We need to convert DataFrame columns into Vectors


# In[121]:


dfClean.head()


# In[124]:


assembler=VectorAssembler(
  inputCols=["postLength","hour"], outputCol="features")


# In[125]:


vectorDf=assembler.transform(dfClean)


# In[126]:


vectorDf.head()


# ## Predicting up votes (5.4)

# In[136]:


from pyspark.ml.regression import RandomForestRegressor,LinearRegression
# This is our regressor
from pyspark.ml.evaluation import RegressionEvaluator
# Module to evaluate fit


# In[127]:


rf=RandomForestRegressor(labelCol="ups", featuresCol="features",numTrees=5)
# This is our regressor="score", featuresCol="features", numTrees=5)
# Create a random forest regressor


# In[39]:


rf=LinearRegression(labelCol="ups", featuresCol="features")
# Create a linear regressor


# In[128]:


(trainingData, testData) = vectorDf.randomSplit([0.7, 0.3])


# In[129]:


model = rf.fit(trainingData)


# In[130]:


predictions = model.transform(testData)


# In[132]:


evaluator = RegressionEvaluator(labelCol="score",         predictionCol="prediction", metricName="mae")
rmse = evaluator.evaluate(predictions)


# In[133]:


print 'Mean absolute error in number of up votes is %.2f' % rmse
# Add in post length


# In[55]:


stringIndexer = StringIndexer(inputCol="subreddit", outputCol="subredditIndex")
model = stringIndexer.fit(dfClean)
indexed = model.transform(dfClean)

#encoder = OneHotEncoder(inputCol="subredditIndex", outputCol="subredditVec")
#encoded = encoder.transform(indexed)


# In[57]:


indexed.head()


# In[64]:


indexed.select(['subredditIndex','subreddit']).head(10)


# ## Convert subredditIndex into vector

# In[68]:


assembler=VectorAssembler(
  inputCols=["subredditIndex"], outputCol="subredditIndexV")


# In[70]:


indexed=assembler.transform(indexed)


# In[123]:


indexed.head(5)


# In[134]:


indexer = StringIndexer(inputCol="subreddit", outputCol="subredditI")
indexedFinal = indexer.fit(df).transform(indexed)


# In[135]:


indexedFinal.head()


# In[154]:


indexedFinal.select('subredditI','subreddit').head(15)


# ## Set >20 =>21

# In[170]:


setIndex=udf(lambda x:int(x) if x<20 else 21,IntegerType())


# In[171]:


indexedFinalCut=indexedFinal.withColumn('indexCut',setIndex('subredditI'))


# In[172]:


indexedFinalCut.head(5)


# ## --

# In[127]:


indexer = VectorIndexer(inputCol="subredditIndexV", outputCol="subredditIndexLim", maxCategories=20)

indexerModel=indexer.fit(indexed)

indexedFinal=indexerModel.transform(indexed)


# In[132]:


indexerModel.extractParamMap()


# In[125]:


categoricalFeatures = indexerModel.categoryMaps
print("Chose %d categorical features: %s" %
      (len(categoricalFeatures), ", ".join(str(k) for k in categoricalFeatures.keys())))


# In[109]:


indexedFinal.head()


# In[117]:


dd=indexedFinal.select(['subredditIndexLim'])


# In[182]:


indexedFinalCut.head()


# ## One-hot encode indexcut

# In[183]:


from pyspark.ml.feature import OneHotEncoder, StringIndexer


# In[184]:


encoder = OneHotEncoder(inputCol="indexCut", outputCol="indexCutHot")
encoded = encoder.transform(indexedFinalCut)
encoded.show()


# ## Assemble into vector

# In[216]:


inputCols=["indexCutHot","postLength","hour"]
inputCols=["postLength",'hour']


# In[217]:


assembler=VectorAssembler(
  inputCols=inputCols, outputCol="featuresFinal")


# In[218]:


ff=assembler.transform(encoded)


# In[219]:


ff.head()


# In[231]:


rf=RandomForestRegressor(labelCol="ups", featuresCol="featuresFinal", numTrees=10)
# Create a random forest regressor


# In[234]:


from pyspark.ml.regression import LinearRegression


# In[243]:


lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8,                      labelCol='ups',featuresCol='featuresFinal')


# In[244]:


(trainingData, testData) = ff.randomSplit([0.7, 0.3])


# In[245]:


model = lr.fit(trainingData)


# In[ ]:


predictions = model.transform(testData)


# In[ ]:


evaluator = RegressionEvaluator(            labelCol="ups", predictionCol="prediction", metricName="mae")
rmse = evaluator.evaluate(predictions)


# In[225]:


print 'Mean absolute error in number of up votes is %.2f' % rmse
# Add in post length


# In[230]:


ff.head()


# In[290]:


from pyspark.sql.functions import udf
stringToVector=udf(lambda x: DenseVector([x]), VectorUDT())


# In[310]:


indexed.head()


# In[315]:


final=indexed.withColumn('subredditV',stringToVector(indexed['subreddit']))


# In[316]:


final.head()


# In[313]:


indexer = VectorIndexer(inputCol="subredditV", outputCol="vSubreddit", maxCategories=10)
indexerModel = indexer.fit(final)


# In[314]:


categoricalFeatures = indexerModel.categoryMaps
print("Chose %d categorical features: %s" %
      (len(categoricalFeatures), ", ".join(str(k) for k in categoricalFeatures.keys())))


# In[ ]:


indexedData = indexerModel.transform(final)


# In[50]:


dfClean.head()


# In[51]:


assembler=VectorAssembler(
  inputCols=["hour","postLength","subreddit"], outputCol="features")


# In[52]:


vectorDf=assembler.transform(dfClean)


# In[299]:


vectorDf.head()


# In[300]:


rf=RandomForestRegressor(labelCol="ups", featuresCol="features", numTrees=1)


# In[301]:


(trainingData, testData) = vectorDf.randomSplit([0.7, 0.3])


# In[302]:


pipeline = Pipeline(stages=[rf])


# In[303]:


model = pipeline.fit(trainingData)


# In[304]:


predictions = model.transform(testData)


# In[305]:


evaluator = RegressionEvaluator(            labelCol="ups", predictionCol="prediction", metricName="mae")
rmse = evaluator.evaluate(predictions)


# In[306]:


print 'Mean absolute error in number of up votes is %.2f' % rmse
# Add in post length


# 4.78 to beat
