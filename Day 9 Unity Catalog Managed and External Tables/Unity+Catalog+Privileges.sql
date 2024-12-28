-- Databricks notebook source

GRANT USE_CATALOG ON CATALOG `dev_catalog` TO `Developers`

-- COMMAND ----------


GRANT SELECT ON CATALOG `dev_catalog` TO `Developers`

-- COMMAND ----------

CREATE TABLE Persons(
PersonID int,
LastName varchar(30),
FirstName varchar(30),
Address varchar(30)
)


-- COMMAND ----------

CREATE TABLE `dev_catalog`.`default`.Persons(
PersonID int,
LastName varchar(30),
FirstName varchar(30),
Address varchar(30)
)


-- COMMAND ----------


