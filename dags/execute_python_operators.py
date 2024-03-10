from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'kai',
}

def taskA():
    print('This is task A')

def taskB():
    print('This is task B')

def taskC():
    print('This is task C')

def taskD():
    print('This is task D')

def greet(name, place):
    print(f'Hello {name} {place}!')

with DAG(
    dag_id='python_operator_dag',
    description='simple python operator DAG',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    tags=['beginner', 'python', 'python operator']
) as dag:
    taskA=PythonOperator(
        task_id='taskA',
        python_callable=greet,
        op_kwargs={'name':'Desmond','place':'Rome'}
    )
    taskB=PythonOperator(
        task_id='taskB',
        python_callable=taskB
    )
    taskC=PythonOperator(
        task_id='taskC',
        python_callable=taskC
    )
    taskD=PythonOperator(
        task_id='taskD',
        python_callable=taskD
    )

taskA >> taskB >> taskC >> taskD