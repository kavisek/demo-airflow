import datetime as dt
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG

default_args = {
    'owner': 'kavi',
    'depends_on_past': False,
    'start_date': dt.datetime(2019, 9, 1),
    'email': ['kavi@donotemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=1),
}

dag = DAG(
    dag_id='update_db_pipeline',
    default_args=default_args,
    schedule_interval='15 * * * *',
    dagrun_timeout=dt.timedelta(minutes=120),
    catchup=True)

# The following bash operators run python scritps
run_cnd_pipeline = BashOperator(task_id='run_cnd_pipeline',
                                bash_command='python ~/scripts/refresh_database.py', dag=dag)

run_usa_pipeline = BashOperator(task_id='run_usa_pipeline',
                                bash_command='python ~/scripts/refresh_database.py', dag=dag)

run_uk_pipeline = BashOperator(task_id='run_uk_pipeline',
                               bash_command='python ~/scripts/refresh_database.py',  dag=dag)


email_notification = BashOperator(task_id='email_notification',
                                  bash_command='echo send email',  dag=dag)

# Dag heirachy of tasks
run_uk_pipeline.set_downstream(email_notification)
run_usa_pipeline.set_downstream(email_notification)
run_cnd_pipeline .set_downstream(email_notification)
