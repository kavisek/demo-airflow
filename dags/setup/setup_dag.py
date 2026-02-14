from datetime import timedelta
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="setup_dag",
    schedule="@once",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["pipeline"],
    params={"example_key": "example_value"},
) as dag:

    # In Airflow 3.x, connections and variables are best defined via
    # environment variables in docker-compose (AIRFLOW_CONN_*, AIRFLOW_VAR_*).
    # This DAG uses the REST API as a fallback to persist them in the database.

    create_connection = BashOperator(
        task_id="create_connection",
        bash_command="""
        curl -s -X POST "http://airflow-apiserver:8080/api/v2/connections" \
            -H "Content-Type: application/json" \
            -u "airflow:airflow" \
            -d '{
                "connection_id": "postgres_default",
                "conn_type": "postgres",
                "host": "postgres",
                "port": 5432,
                "schema": "postgres",
                "login": "airflow",
                "password": "airflow",
                "extra": "{\\"sslmode\\": \\"disable\\"}"
            }' && echo " Connection created successfully" || echo " Connection may already exist"
        """,
    )

    create_variable = BashOperator(
        task_id="create_variable",
        bash_command="""
        curl -s -X POST "http://airflow-apiserver:8080/api/v2/variables" \
            -H "Content-Type: application/json" \
            -u "airflow:airflow" \
            -d '{
                "key": "environment",
                "value": "local"
            }' && echo " Variable created successfully" || echo " Variable may already exist"
        """,
    )

    create_connection >> create_variable
