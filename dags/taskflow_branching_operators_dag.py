from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

from airflow.models import Variable

import pandas as pd

default_args={
    'owner':'kai'
}

@dag(
    dag_id='taskflow_branching_operators_dag',
    description='Simple DAG with TaskFlow API and Branching Operators',
    start_date=days_ago(1),
    schedule_interval='@daily',
    default_args=default_args,
    tags=['beginner', 'taskflow', 'branching']
)
def taskflow_branching_dag():

    @task(task_id='read_data')
    def read_data():
        print('This is task A')
        df=pd.read_csv('/home/kai/airflow/dags/datasets/data.csv')
        print(df)
        return df.to_json()
    
    @task
    def clean_data(ti):
        data=ti.xcom_pull(task_ids='read_data')
        print('This is task B')
        df=pd.read_json(data)
        df.dropna(inplace=True)
        ti.xcom_push(key='clean_data',value=df.to_json())
    
    @task.branch
    def branch():
        print('branching')
        turn=Variable.get('turn', default_var=None)
        if turn=='car':
            return 'filter_by_car'
        else:
            return 'filter_by_weight'
    
    @task(task_id='filter_by_car')
    def filter_by_car(**kwargs):
        ti=kwargs['ti']
        print('This is task C')
        df=pd.read_json(ti.xcom_pull(key='clean_data'))
        df=df[df['Car']=='Ford']
        ti.xcom_push(key='filtered_data',value=df.to_json())
        ti.xcom_push(key='filtered_title',value='filter_by_car')
    
    @task(task_id='filter_by_weight')
    def filter_by_weight(**kwargs):
        ti=kwargs['ti']
        print('This is task C')
        df=pd.read_json(ti.xcom_pull(key='clean_data'))
        df=df[df['Weight']>300]
        ti.xcom_push(key='filtered_data',value=df.to_json())
        ti.xcom_push(key='filtered_title',value='filter_by_weight')
    
    @task(trigger_rule='none_failed')
    def write_csv(**kwargs):
        ti=kwargs['ti']
        print('This is task D')
        data=ti.xcom_pull(key='filtered_data')
        title=ti.xcom_pull(key='filtered_title')
        df=pd.read_json(data)
        df.to_csv('airflow/dags/datasets/{0}.csv'.format(title), index=False)
    
    read_data() >> clean_data() >> branch() >> [filter_by_car(), filter_by_weight()] >> write_csv()

taskflow_branching_dag()
