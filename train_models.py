# Import modules
import datetime as dt
import os
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG

# The default arguments for our DaG
default_args = {
    'owner': 'kavi sekhon',
    'depends_on_past': False,
    'start_date': dt.datetime(2018, 10, 11),
    'email': ['kavi.skhon@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': dt.timedelta(minutes=5),
}

# Obstinate a DAG variable
# Run the DAG once a day at midnight
dag = DAG(
    dag_id='kavi_train_models',
    default_args=default_args,
    schedule_interval='00 00 * * *',
    dagrun_timeout=dt.timedelta(minutes=15))

# A list of functions our model training (Notebbook Trainer)


def find_paths(path):
    '''
    Search the given directory for all the files within that directory.

    Parameter
    ---------
    path: absolute path to the directory to search withing (str)

    Example
    --------
    >>>> find_path(/Users/Kavi/Documents/Science')
    '''
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file = file.replace(' ', '\ ')
            paths.append(root+file)
    return paths


def run_notebook_cells(paths):
    '''
    Train Every Notebook within list of paths this function recieves.

    Parameter
    ---------
    path: absolute paths to each notebook file to run_notebooks

    Example
    --------
    >>>> run_notebooks(notebook_paths)

    '''
    for path in paths:
        command = ('jupyter nbconvert --execute --to ' + path
                   + ' --inplace ' + path)
        os.system(command)


def train_models(path):
    '''
    A single function to locate and train our notebooks using the functions
    above.

    Parameters
    ----------
    Path: the path arguments to pass down to our "find paths" function

    Example
    ----------
    >>>> train_models(/Users/Kavi/Documents/Airflow/Models/Train/)
    '''
    notebook_paths = find_paths(path)
    run_notebook_cells(notebook_paths)


# Run our model trainer
run_model_trainer = PythonOperator(
    task_id='Locate_Notebook_File_Paths',
    python_callable=train_models,
    op_kwargs={'path': '/Users/Kavi/Documents/Airflow/Models/Train/'},
    dag=dag,
)
