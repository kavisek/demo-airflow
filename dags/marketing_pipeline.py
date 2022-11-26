import datetime as dt
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG

default_args = {
    'owner': 'kavi',
    'depends_on_past': False,
    'start_date': dt.datetime(2022, 9, 1),
    'email': ['airflow_owner@donotemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=1),
}

dag = DAG(
    dag_id='marketing_pipeline',
    default_args=default_args,
    schedule_interval='0 3 * * *',
    dagrun_timeout=dt.timedelta(minutes=120),
    catchup=True)


run_google_ads = BashOperator(task_id='run_google_ads',
                              bash_command='echo running\ google\ ads\ pipeline', dag=dag)

run_facebook = BashOperator(task_id='run_facebook',
                            bash_command='echo running\ facebook\ ads\ pipeline', dag=dag)
