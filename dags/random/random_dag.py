from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import random
from datetime import datetime, timedelta
import datetime

import pendulum

# Define default_args dictionary to specify default parameters of the DAG
# Create a DAG object
with DAG(
    "random_dependency",
    schedule="@daily",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["pipeline"],
    params={"example_key": "example_value"},
) as dag:

    t0 = DummyOperator(task_id='start')
    tx = DummyOperator(task_id='end')

    for i in range(0,random.randint(2, 5)):
        t = DummyOperator(task_id='task_' + str(i))
        t0 >> t >> tx


