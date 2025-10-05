# ML service

### Parts:
1. Postgres database (data from mlflow, airflow)
2. Redis (cache for airflow)
3. Minio (s3 storage for store model)
4. Clickhouse database (main data storage, сolumn-oriented database)
5. Init container (for creating needed databases, for mlflow and airflow, and for loading data to clickhouse database from csv)
6. Mlflow (machine learning logging and control)
7. Airflow (checkpoints for retraining the model)
8. Spark (teaching the model)
9. AkkaHTTP (backend service)
10. React (frontend service)

#### Postgresql for mlflow and airflow data

I use only one database for both mlflow and airfllow data. Also I want to use one redis service as airflow default cache and as cache in main part of my project. 
 
#### Clickhouse 

> I choose clickhouse as source database because it more suitable for data analysis. Spark was also my choice because it's designed for processing large volumes of data. In past I've previously worked with PySpark and for this project I would like to diving into Scala language.

#### What about Makefile?
For more comfortable using I wrote Makefile that run many docker-compose.yml files and check whether runnig containers are healthy.