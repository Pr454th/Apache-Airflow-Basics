import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'kai',
}

def read_csv_file():
    print('This is task A')
    df=pd.read_csv('dags/datasets/insurance.csv')
    print(df)
    return df.to_json()

def remove_null_values(**kwargs):
    print('This is task B')
    ti=kwargs['ti']
    json_data=ti.xcom_pull(task_ids='taskA')
    df=pd.read_json(json_data)
    df.dropna(inplace=True)
    return df.to_json()

def groupby_gender(ti):
    print('This is task C')
    json_data=ti.xcom_pull(task_ids='taskB')
    df=pd.read_json(json_data)
    df=df.groupby('Gender').agg({'Age':'mean','Premium':'mean','Deductible':'mean'}).reset_index()
    df.to_csv('dags/datasets/groupby_gender.csv')

def groupby_smoker(ti):
    print('This is task D')
    json_data=ti.xcom_pull(task_ids='taskB')
    df=pd.read_json(json_data)
    df=df.groupby('Smoker').agg({'Age':'mean','Premium':'mean','Deductible':'mean'}).reset_index()
    df.to_csv('dags/datasets/groupby_smoker.csv')

with DAG(
    dag_id='python_pipeline_dag',
    description='simple python pipeline DAG',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    tags=['beginner', 'python', 'python pipeline', 'transform']
) as dag:
    taskA=PythonOperator(
        task_id='taskA',
        python_callable=read_csv_file
    )
    taskB=PythonOperator(
        task_id='taskB',
        python_callable=remove_null_values
    )
    taskC=PythonOperator(
        task_id='taskC',
        python_callable=groupby_gender
    )
    taskD=PythonOperator(
        task_id='taskD',
        python_callable=groupby_smoker
    )
    
taskA >> taskB >> [taskC, taskD]