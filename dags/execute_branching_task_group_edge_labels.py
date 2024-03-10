import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.edgemodifier import Label
from airflow.utils.task_group import TaskGroup

DATASET_PATH='dags/datasets/insurance.csv'
OUTPUT_PATH='dags/datasets/{0}.csv'

default_args = {
    'owner': 'kai',
}

def read_csv_file(ti):
    print('This is task A')
    df=pd.read_csv('dags/datasets/insurance.csv')
    print(df)
    ti.xcom_push(key='csv_data',value=df.to_json())

def remove_null_values(**kwargs):
    print('This is task B')
    ti=kwargs['ti']
    json_data=ti.xcom_pull(key='csv_data')
    df=pd.read_json(json_data)
    df.dropna(inplace=True)
    ti.xcom_push(key='clean_data',value=df.to_json())

def branch():
    print('branch')
    transform_action=Variable.get('transform_action', default_var=None)
    print(transform_action)
    if transform_action.startswith('filter'):
        return 'Filtering.{0}'.format(transform_action)
    elif transform_action=='groupby_gender':
        return f'grouping.{transform_action}'
    else:
        return groupby_smoker

def filter_by_coverage(ti):
    print('filtering by coverage')
    json_data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(json_data)
    df=df[df['Coverage']=='Basic']
    return df.to_json(
        OUTPUT_PATH.format('filter_by_coverage'),
        index=False
    )

def filter_by_location(ti):
    print('filtering by location')
    json_data=ti.xcom_pull(key='clean_data')
    df=pd.read.json(json_data)
    df=df[df['Location']=='Rural']
    return df.to_json(
        OUTPUT_PATH.format('filter_by_location'),
        index=False
    )

def groupby_gender(ti):
    print('This is task C')
    json_data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(json_data)
    df=df.groupby('Gender').agg({'Age':'mean','Premium':'mean','Deductible':'mean'}).reset_index()
    df.to_csv(
        OUTPUT_PATH.format('groupby_gender'),
        index=False
    )

def groupby_smoker(ti):
    print('This is task D')
    json_data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(json_data)
    df=df.groupby('Smoker').agg({'Age':'mean','Premium':'mean','Deductible':'mean'}).reset_index()
    df.to_csv(
        OUTPUT_PATH.format('groupby_smoker'),
        index=False
    )

with DAG(
    dag_id='pipeline_task_groups_edge_labels_dag',
    description='simple python pipeline DAG with Task Groups and Edge Labels',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    tags=['beginner', 'python', 'branch python pipeline', 'transform','task groups','edge labels']
) as dag:
    with TaskGroup('reading_and_preprocessing') as read_and_preprocessing:
        taskA=PythonOperator(
            task_id='taskA',
            python_callable=read_csv_file
        )
        taskB=PythonOperator(
            task_id='taskB',
            python_callable=remove_null_values
        )
        taskA >> taskB
        
    taskE=BranchPythonOperator(
        task_id='branch',
        python_callable=branch
    )

    with TaskGroup('Grouping') as grouping:
        taskC=PythonOperator(
            task_id='groupby_gender',
            python_callable=groupby_gender
        )
        taskD=PythonOperator(
            task_id='groupby_smoker',
            python_callable=groupby_smoker
        )

    with TaskGroup('Filtering') as filtering:
        taskF=PythonOperator(
            task_id='filter_by_coverage',
            python_callable=filter_by_coverage
        )
        taskG=PythonOperator(
            task_id='filter_by_location',
            python_callable=filter_by_location
        )
    
read_and_preprocessing >> Label('preprocessed data') >> taskE >> Label('branch on condition') >> [grouping,filtering]