# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ### Running common notebook to get access to variables

# COMMAND ----------

# MAGIC %run "/Users/shanmukh@shanmukhsattiraju.com/04. Common"

# COMMAND ----------

dbutils.widgets.text(name="env",defaultValue='',label='Enter the environment in lower case')
env = dbutils.widgets.get("env")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Reading from bronze raw_Roads

# COMMAND ----------


def read_BronzeRoadsTable(environment):
    print('Reading the Bronze Table raw_roads Data : ',end='')
    df_bronzeRoads = (spark.readStream
                    .table(f"`{environment}_catalog`.`bronze`.raw_roads")
                    )
    print(f'Reading {environment}_catalog.bronze.raw_roads Success!')
    print("**********************************")
    return df_bronzeRoads

# COMMAND ----------

df_roads = read_BronzeRoadsTable(env)

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Creating road_category_name column

# COMMAND ----------

def road_Category(df):
    print('Creating Road Category Name Column: ', end='')
    from pyspark.sql.functions import when,col

    df_road_Cat = df.withColumn("Road_Category_Name",
                  when(col('Road_Category') == 'TA', 'Class A Trunk Road')
                  .when(col('Road_Category') == 'TM', 'Class A Trunk Motor')
                   .when(col('Road_Category') == 'PA','Class A Principal road')
                    .when(col('Road_Category') == 'PM','Class A Principal Motorway')
                    .when(col('Road_Category') == 'M','Class B road')
                    .otherwise('NA')
                  
                  )
    print('Success!! ')
    print('***********************')
    return df_road_Cat

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Creating road_type column
# MAGIC
# MAGIC

# COMMAND ----------

def road_Type(df):
    print('Creating Road Type Name Column: ', end='')
    from pyspark.sql.functions import when,col

    df_road_Type = df.withColumn("Road_Type",
                  when(col('Road_Category_Name').like('%Class A%'),'Major')
                  .when(col('Road_Category_Name').like('%Class B%'),'Minor')
                    .otherwise('NA')
                  
                  )
    print('Success!! ')
    print('***********************')
    return df_road_Type

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Writing data to silver_roads in Silver schema

# COMMAND ----------

def write_Roads_SilverTable(StreamingDF,environment):
    print('Writing the silver_roads Data : ',end='') 

    write_StreamSilver_R = (StreamingDF.writeStream
                .format('delta')
                .option('checkpointLocation',checkpoint+ "/SilverRoadsLoad/Checkpt/")
                .outputMode('append')
                .queryName("SilverRoadsWriteStream")
                .trigger(availableNow=True)
                .toTable(f"`{environment}_catalog`.`silver`.`silver_roads`"))
    
    write_StreamSilver_R.awaitTermination()
    print(f'Writing `{environment}_catalog`.`silver`.`silver_roads` Success!')

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Calling functions

# COMMAND ----------

df_noDups = remove_Dups(df_roads)

AllColumns = df_noDups.schema.names
df_clean = handle_NULLs(df_noDups,AllColumns)

## Creating Road_Category_name 
df_roadCat = road_Category(df_clean)

## Creating Road_Type column
df_type = road_Type(df_roadCat)

## Writing data to silver_roads table

write_Roads_SilverTable(df_type,env)

# COMMAND ----------

