import datetime

import pendulum

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.bash_operator import BashOperator

# TODO: To get this dag working. You need to set up a`
# postgres_default connection in the Airflow UI. Admin -> Connections -> Create

# There is a scritp

with DAG(
    dag_id="postgres_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["example", "example2"],
    params={"example_key": "example_value"},
) as dag:

    create_table = PostgresOperator(
        postgres_conn_id="postgres_default",
        retries=2,
        retry_delay=datetime.timedelta(seconds=5),
        task_id="create_table",
        sql="""
            CREATE TABLE IF NOT EXISTS example_table (
                id SERIAL PRIMARY KEY,
                event_name VARCHAR(50) NOT NULL,
                event_value INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL
            );
            """,
    )

    populate_table = PostgresOperator(
        postgres_conn_id="postgres_default",
        retries=2,
        retry_delay=datetime.timedelta(seconds=5),
        task_id="populate_table",
        sql="""
            INSERT INTO example_table (event_name, event_value, created_at) VALUES ('example', 1, NOW());
            """,
    )

    get_table = PostgresOperator(
        postgres_conn_id="postgres_default",
        retries=2,
        retry_delay=datetime.timedelta(seconds=5),
        task_id="get_table",
        sql="""
            SELECT * FROM example_table;
            """,
    )


if __name__ == "__main__":
    dag.cli()
