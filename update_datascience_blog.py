# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import airflow
import datetime as dt
from builtins import range
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG


default_args = {
    'owner': 'kavi sekhon',
    'depends_on_past': False,
    'start_date': dt.datetime(2018, 9, 20),
    'email': ['kavi.skhon@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 5,
    'retry_delay': dt.timedelta(minutes=1),
}

dag = DAG(
    dag_id='update_website_content', default_args=default_args,
    schedule_interval='00 10 * * *',
    dagrun_timeout=dt.timedelta(minutes=60*7))

run_first = BashOperator(task_id='Locating_Blog_Folder',
                         bash_command='cd /Users/kavi/Documents/Blog/', dag=dag)

run_second = BashOperator(task_id='Run_Content_Movement_Script',
                          bash_command='python /Users/kavi/Documents/Blog/update.py', dag=dag)

run_first.set_downstream(run_second)

run_third = BashOperator(task_id='Activate_Conda_Main',
                         bash_command='source activate main', dag=dag)

run_second.set_downstream(run_third)

# Bash Script require a space after .sh
run_fourth = BashOperator(task_id='Run_Pelican_Content',
                          bash_command='source activate main && bash /Users/kavi/Documents/Blog/update.sh ', dag=dag)

run_third.set_downstream(run_fourth)

if __name__ == "__main__":
    dag.cli()
