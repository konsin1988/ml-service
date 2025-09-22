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