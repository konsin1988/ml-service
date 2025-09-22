import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import clickhouse_connect
from minio import Minio


class Init:
    def __init__(self):
        self.__set_engine_and_client()
        self.__use_database()
        self.__check_empty()

    def __get_environ(self):
        load_dotenv()
        return {"pg_user": os.getenv("PG_USER"),
                "pg_password": os.getenv("PG_PASSWORD"),
                "pg_host": os.getenv("PG_HOST"),
                # "pg_host": "localhost",
                "pg_port": os.getenv("PG_PORT"),
                "pg_database": os.getenv("PG_NAME"),
                "click_user": os.getenv("CLICKHOUSE_USER"),
                "click_password": os.getenv("CLICKHOUSE_PASSWORD"),
                "click_host": os.getenv("CLICKHOUSE_HOST"),
                # "click_host": "localhost",
                "click_port": os.getenv("CLICKHOUSE_PORT"),
                "click_database": os.getenv("CLICKHOUSE_DB"),
                "minio_endpoint": os.getenv("MLFLOW_S3_ENDPOINT_URL"),
                # "minio_endpoint": "localhost:9099",
                "access_key": os.getenv("MINIO_ROOT_USER"),
                "secret_key": os.getenv("MINIO_ROOT_PASSWORD")
               }

    def __set_engine_and_client(self):
        EV = self.__get_environ()
        self.__engine = create_engine(f"postgresql+psycopg2://{EV['pg_user']}:{EV['pg_password']}@{EV['pg_host']}:{EV['pg_port']}/{EV['pg_database']}")
        self.__click_client = clickhouse_connect.get_client(host=EV['click_host'], 
                                                      port=EV['click_port'], 
                                                      username=EV['click_user'], 
                                                      password=EV['click_password'],
                                                     database=EV['click_database'])
        self.__minio_client = Minio(
            EV['minio_endpoint'],
            access_key=EV['access_key'],
            secret_key=EV['secret_key'],
            secure=False  # Set to False if using HTTP
        )
        self.__use_database()

    def __get_list_files(self):
        return os.listdir('/data/')

    def __use_database(self):
        query = r'USE wb_orders'
        self.__click_client.command(query)

    def __check_empty(self):
        query = "EXISTS TABLE wb_orders;"
        self.__is_empty = True if self.__click_client.command(query) == 0 else False

    def create_clickhouse_table(self):
        if self.__is_empty:
            query = r'''
                CREATE TABLE IF NOT EXISTS wb_orders (
                    date DateTime,
                    last_change_date DateTime, 
                    total_price Float32, 
                    discount_percent Int8,
                    warehouse_name String, 
                    oblast Nullable(String), 
                    nm_id Int64, 
                    category String, 
                    brand String, 
                    is_cancel Bool,
                    cancel_dt Nullable(DateTime), 
                    created_at Nullable(DateTime), 
                    updated_at DateTime, 
                    order_type Nullable(String)
                    ) ENGINE = MergeTree PARTITION BY toYYYYMM(date) ORDER BY date SETTINGS index_granularity = 2048 
                '''
            self.__click_client.command(query)
            print("Table created successfully")
        else:
            print("Table already exists. Pass.")
        query = r'DROP DATABASE IF EXISTS default;'
        self.__click_client.command(query)

    def load_data(self):
        if self.__is_empty:
            df = pd.read_csv('/data/wb_orders.csv', 
                             parse_dates=['date', 'last_change_date', 'created_at', 'updated_at', 'cancel_dt'], 
                             dayfirst=True, decimal=',')
            self.__click_client.insert_df('wb_orders.wb_orders', df)
            print('Data loaded successfully')
        
    def __get_list_databases(self):
        query = "SELECT datname FROM pg_database;"
        return pd.read_sql_query(query, self.__engine)['datname'].to_list()

    def create_postgres_database(self):
        db_name = 'airflow'
        if db_name not in self.__get_list_databases():
            query = text("Create user airflow with password 'airflow';") 
            with self.__engine.connect() as con:
                con.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                con.execute(query)
            query = text(f'Create database {db_name} owner airflow')
            with self.__engine.connect() as con:
                con.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                con.execute(query)
            query = text("grant all privileges on database airflow to airflow")
            with self.__engine.connect() as con:
                con.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                con.execute(query)
        if "postgres" in self.__get_list_databases():
            query = r'drop database postgres;'
            with self.__engine.connect() as con:
                con.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                con.execute(text(query))

    def create_minio_mlflow_bucket(self):
        bucket_name = 'mlflow'
        if not self.__minio_client.bucket_exists(bucket_name):
            self.__minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
        

def main():
    init = Init()
    init.create_clickhouse_table()
    init.load_data()
    init.create_postgres_database()
    init.create_minio_mlflow_bucket()

if __name__ == "__main__":
    main()
