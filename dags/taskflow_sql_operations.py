from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.sqlite_operator import SqliteOperator
import pandas as pd

from datetime import datetime, timedelta

default_args={
    'owner':'kai'
}

@dag(
    dag_id='taskflow_sql_operations_dag',
    description='Simple DAG SQL operations',
    start_date=days_ago(1),
    schedule_interval='@daily',
    default_args=default_args,
    tags=['beginner', 'taskflow']
)
def taskflow_sql_operations_pipeline():
    @task(task_id='read_task')
    def read_csv():
        print('Reading CSV file')
        df=pd.read_csv('/home/kai/airflow/dags/datasets/data.csv')
        return df.to_json()

    @task
    def create_table():
        sqlite_operator=SqliteOperator(
            task_id='create_table',
            sqlite_conn_id='my_sqlite_conn',
            sql='''
            CREATE TABLE IF NOT EXISTS Car (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                model TEXT NOT NULL,
                volume INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                co2 INTEGER NOT NULL
            )
            '''
        )
        sqlite_operator.execute(context=None)
    
    @task
    def insert_records(**kwargs):
        print('This is task C')
        ti=kwargs['ti']
        data=ti.xcom_pull(task_ids='read_task')
        df=pd.read_json(data)
        for row in df.itertuples():
            sqlite_operator=SqliteOperator(
                task_id='insert_record',
                sqlite_conn_id='my_sqlite_conn',
                sql=f'''
                INSERT INTO Car (name, model, volume, weight, co2)
                VALUES ('{row.Car}', '{row.Model}', {row.Volume}, {row.Weight}, {row.CO2})
                '''
            )
            sqlite_operator.execute(context=None)
    
    @task
    def insert_dummy_records():
        sqlite_operator=SqliteOperator(
            task_id='insert_dummy_records',
            sqlite_conn_id='my_sqlite_conn',
            sql='''
            INSERT INTO Car (name, model, volume, weight, co2)
            VALUES ('Ford', 'Focus', 1000, 200, 100)
            '''
        )
        sqlite_operator.execute(context=None)

    @task
    def join():
        sqlite_operator=SqliteOperator(
            task_id='join',
            sqlite_conn_id='my_sqlite_conn',
            sql='''
            SELECT * FROM Car
            '''
        )
        sqlite_operator.execute(context=None)

    join_task=join()

    read_csv() >> create_table() >> join_task
    insert_records() >> join_task
    insert_dummy_records() >> join_task

taskflow_sql_operations_pipeline()