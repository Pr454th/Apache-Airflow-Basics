from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

import json

default_args={
    'owner':'kai'
}

@dag(
    dag_id='xcom_taskflow_dag',
    description='Simple dag with xcom',
    default_args=default_args,
    start_date=days_ago(2),
    schedule_interval='@daily',
    tags=['beginner', 'taskflow', 'xcom']
)
def xcom_taskflow_dag():
    @task
    def push_function():
        prices={
            'oranges': 0.50,
            'apples': 0.40,
            'pears': 0.60,
            'bananas': 0.70,
            'grapes': 1.00
        }
        return prices
    
    @task(multiple_outputs=True)
    def compute_purchase(prices: dict):
        purchase={}
        total=0
        for fruit, price in prices.items():
            total+=price
        avg=total/len(prices)
        purchase['Total']=total
        purchase['Average']=avg
        return purchase
    
    @task
    def notify(total, average):
        print(f'Total price: {total}')
        print(f'Average price: {average}')

    prices=push_function()

    purchase=compute_purchase(prices)
    
    notify(purchase['Total'], purchase['Average'])

xcom_taskflow_dag()