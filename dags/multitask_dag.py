from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'kai',
}

with DAG(
    dag_id='multitask_dag',
    description='Multitask DAG',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    tags=['beginner', 'bash', 'multitask'],
    template_searchpath=['dags/bash_scripts']
) as dag:
    
        taskA=BashOperator(
            task_id='taskA',
            bash_command='taskA.sh'
        )
    
        taskB=BashOperator(
            task_id='taskB',
            bash_command='taskB.sh'
        )
    
        taskC=BashOperator(
            task_id='taskC',
            bash_command='taskC.sh'
        )
    
        taskD=BashOperator(
            task_id='taskD',
            bash_command='taskD.sh'
        )

        taskE=BashOperator(
            task_id='taskE',
            bash_command='taskE.sh'
        )

taskA >> [taskB, taskC] >> taskD >> taskE