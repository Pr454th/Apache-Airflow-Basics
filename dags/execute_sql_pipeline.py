from airflow import DAG
from airflow.operators.sqlite_operator import SqliteOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'kai',
}

with DAG(
    dag_id='sql_operator_dag',
    description='simple sql operator DAG',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    tags=['beginner', 'python', 'sql operator']
) as dag:
    createTable=SqliteOperator(
        task_id='taskA',
        sql=
        r"""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            place TEXT NOT NULL
        );""",
        sqlite_conn_id='my_sqlite_conn'
    )

    insertData=SqliteOperator(
        task_id='taskB',
        sql=
        r"""
            INSERT INTO students (name, age, place) VALUES 
            ('Desmond', 25, 'Rome'),
            ('Kai', 24, 'Berlin'),
            ('John', 26, 'Paris'),
            ('Micheal', 27, 'London'),
            ('Sara', 28, 'Madrid');
        """,
        sqlite_conn_id='my_sqlite_conn'
    )

    displayData=SqliteOperator(
        task_id='taskC',
        sql=
        r"""
            SELECT * FROM students;
        """,
        sqlite_conn_id='my_sqlite_conn',
        do_xcom_push=True
    )

    updateData=SqliteOperator(
        task_id='taskD',
        sql=
        r"""
            UPDATE students SET age=age+1 where age>25;
        """,
        sqlite_conn_id='my_sqlite_conn'
    )

    deleteData=SqliteOperator(
        task_id='taskE',
        sql=
        r"""
            DELETE FROM students WHERE age<25;
        """,
        sqlite_conn_id='my_sqlite_conn'
    )

createTable >> insertData >> updateData >> deleteData >> displayData