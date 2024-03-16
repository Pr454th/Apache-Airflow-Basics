from airflow.utils.dates import days_ago
from airflow.decorators import dag, task

from datetime import datetime, timedelta

default_args={
    'owner':'kai'
}

@dag(
    dag_id='simple_dag_with_taskflow',
    description='Simple DAG with TaskFlow API',
    start_date=days_ago(1),
    schedule_interval='@daily',
    default_args=default_args,
    tags=['beginner', 'taskflow']
)
def dag_with_taskflow_api():
    @task
    def task_a():
        print('This is task A')
    
    @task
    def task_b():
        print('This is task B')
    
    @task
    def task_c():
        print('This is task C')

    @task
    def task_d():
        print('This is task D')

    task_a() >> [task_b(), task_c()] >> task_d()

dag_with_taskflow_api()