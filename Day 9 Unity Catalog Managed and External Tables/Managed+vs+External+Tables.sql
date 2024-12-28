-- Databricks notebook source
-- MAGIC %md
-- MAGIC
-- MAGIC ## Creating a managed table

-- COMMAND ----------


CREATE TABLE `dev_catalog`.`default`.Person_Table
(
  Person_ID  INT,
  FirstName  STRING,
  LastName  STRING
);


-- COMMAND ----------

INSERT INTO `dev_catalog`.`default`.Person_Table
VALUES
  (10, 'Steve', 'Rogers'),
  (20, 'Tony', 'Stark'),
  (30, 'Shanmukh', 'Sattiraju');


-- COMMAND ----------

describe extended `dev_catalog`.`default`.Person_Table

-- COMMAND ----------

DROP TABLE `dev_catalog`.`default`.Person_Table

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## External tables

-- COMMAND ----------

SHOW EXTERNAL LOCATIONS;

-- COMMAND ----------

DESCRIBE EXTERNAL LOCATION deltastoragelocation

-- COMMAND ----------

CREATE TABLE `dev_catalog`.`default`.Person_External
(
    Education_Level STRING,
    Line_Number INT,
    Employed INT,
    Unemployed INT,
    Industry STRING,
    Gender STRING,
    Date_Inserted STRING,
    dense_rank INT)
USING CSV
OPTIONS(
  'header' 'true'
)
LOCATION 'abfss://test@deltadbstg.dfs.core.windows.net/files'

-- COMMAND ----------

SELECT * FROM `dev_catalog`.`default`.Person_External

-- COMMAND ----------

DESCRIBE EXTENDED `dev_catalog`.`default`.Person_External

-- COMMAND ----------

drop table `dev_catalog`.`default`.Person_External

-- COMMAND ----------


