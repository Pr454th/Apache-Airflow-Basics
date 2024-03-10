from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'kai',
}

def taskA(a,b):
    print('Task A: starting point to add two numbers')
    return a+b;

def taskB(ti):
    print('Task B: starting point to multiply the result of task A by 10')
    value=ti.xcom_pull(task_ids='taskA')
    return value*10

def taskC(ti):
    print('Task C: starting point to subtract the result of task B by 3')
    value=ti.xcom_pull(task_ids='taskB')
    return value-3

with DAG(
    dag_id='cross_task_dag',
    description='simple python operator DAG',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    tags=['beginner', 'python', 'python operator']
) as dag:
    taskA=PythonOperator(
        task_id='taskA',
        python_callable=taskA,
        op_kwargs={'a':5,'b':5}
    )
    taskB=PythonOperator(
        task_id='taskB',
        python_callable=taskB
    )
    taskC=PythonOperator(
        task_id='taskC',
        python_callable=taskC
    )

taskA >> taskB >> taskC