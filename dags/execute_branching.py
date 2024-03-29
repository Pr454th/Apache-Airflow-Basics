from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from random import choice

default_args = {
    'owner': 'kai',
}

def is_over_18():
    print('This is task A')
    return choice([True, False])

def branch(ti):
    print('This is task B')
    if ti.xcom_pull(task_ids='over_18'):
        return 'eligible_to_vote'
    else:
        return 'not_eligible_to_vote'

def eligible_to_vote():
    print('Eligible to Vote')

def not_eligible_to_vote():
    print('Not Eligible to Vote')

with DAG(
    dag_id='branching_dag',
    description='simple python branch operator DAG',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    tags=['beginner', 'python', 'branch python operator']
) as dag:
    
    taskA=PythonOperator(
        task_id='over_18',
        python_callable=is_over_18,
        op_kwargs={'name':'Desmond','place':'Rome'}
    )

    taskB=BranchPythonOperator(
        task_id='branch',
        python_callable=branch
    )

    taskC=PythonOperator(
        task_id='eligible_to_vote',
        python_callable=eligible_to_vote
    )

    taskD=PythonOperator(
        task_id='not_eligible_to_vote',
        python_callable=not_eligible_to_vote
    )

taskA >> taskB >> [taskC, taskD]