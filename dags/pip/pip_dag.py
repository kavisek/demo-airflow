import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="pip_dag",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["example", "example2"],
    params={"example_key": "example_value"},
) as dag:

    # [START howto_operator_bash]
    run_this = BashOperator(
        task_id="running_pip_requirements",
        bash_command="pip3 list",
    )

if __name__ == "__main__":
    dag.cli()
