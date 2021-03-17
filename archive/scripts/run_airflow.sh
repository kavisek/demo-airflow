source activate airflow
export AIRFLOW_HOME="/root"

airflow db init

while echo "Running Airflow Scheduler..."; do
  # Failure: Logging date txt file
  date >> "$(pwd)"/logs/airflow_scheduler.log
  airflow scheduler -n 10
  echo "sleep for 1 second...."
  sleep 1
done
