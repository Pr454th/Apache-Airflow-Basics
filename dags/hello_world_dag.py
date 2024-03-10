from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'kai',
}

with DAG(
    dag_id='hello_world',
    description='Siple Hello world DAG',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    tags=['beginner', 'bash', 'hello world']
) as dag:

    taskA=BashOperator(
        task_id='taskA',
        bash_command=
        '''
            echo Welcome to Task A
            sleep 20
            echo End of Task A
        '''
    )

    taskB=BashOperator(
        task_id='taskB',
        bash_command=
        '''
            echo Welcome to Task B
            sleep 30
            echo End of Task B
        '''
    )

    taskC=BashOperator(
        task_id='taskC',
        bash_command=
        '''
            echo Welcome to Task C
            sleep 20
            echo End of Task C
        '''
    )

    taskD=BashOperator(
        task_id='taskD',
        bash_command=
        '''
            echo Welcome to Task D
            sleep 30
            echo End of Task D
        '''
    )

taskA >> [taskB, taskC] >> taskD


# taskA.set_downstream(taskB)
# taskA.set_downstream(taskC)

# taskD.set_upstream(taskB)
# taskD.set_upstream(taskC)