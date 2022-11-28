import datetime

import pendulum

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.bash_operator import BashOperator


with DAG(
    dag_id="setup_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["example", "example2"],
    params={"example_key": "example_value"},
) as dag:

    create_connection = BashOperator(
        task_id="create_connection",
        bash_command="""
        airflow connections add 'postgres_default' \
        --conn-json '{
            "conn_type": "postgres",
            "host": "postgres", 
            "port": 5432, 
            "schema": "postgres", 
            "login": "airflow", 
            "password": "airflow", 
            "extra": { "sslmode": "disable" }
        }'
        """,
    )