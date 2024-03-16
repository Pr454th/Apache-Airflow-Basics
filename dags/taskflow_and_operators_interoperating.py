from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

default_args={
    'owner':'kai'
}

@dag(
    dag_id='taskflow_and_operators_interoperating',
    description='Simple DAG with TaskFlow API and Operators',
    start_date=days_ago(1),
    schedule_interval='@daily',
    default_args=default_args,
    tags=['beginner', 'taskflow', 'operators']
)
def taskflow_and_operators_interoperating():

    def task_a(**kwargs):
        print('This is task A')
        ti=kwargs['ti']
        ti.xcom_push(key='message', value='task A')
    
    @task
    def task_b(message:str):
        print('This is task B')
        print(message)
        return 'task B'
    
    def task_c(data):
        print('This is task C', data)

    taskA=PythonOperator(
        task_id='task_a',
        python_callable=task_a
    )

    data=task_b(taskA.output['message'])

    taskC=PythonOperator(
        task_id='task_c',
        python_callable=task_c,
        op_kwargs={'data':data}
    )

taskflow_and_operators_interoperating()