import airflow
from builtins import range
import datetime as dt
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG

default_args = {
    'owner': 'kavi sekhon',
    'depends_on_past': False,
    'start_date': dt.datetime(2018, 10, 11),
    'email': ['kavi.skhon@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=1),
}

dag = DAG(
    dag_id='kavi_update_log',
    default_args=default_args,
    schedule_interval='* 1 * * *',
    dagrun_timeout=dt.timedelta(minutes=15))


def append_log():
    '''Append timestamp to the Airflow Custom Log Directory

    Parameters
    ----------
    None

    Example
    ----------
    append_log()'''

    path = '/Users/kavi/Documents/Airflow/Logs/'
    with open(path + 'log.txt', 'a') as log_file:
        dt_time = str(dt.datetime.now())
        log_file.write('\n This script last ran at: ' + dt_time)


run_first = PythonOperator(
    task_id='Run_Appending_Log_Script2',
    python_callable=append_log,
    dag=dag,
)
