sleep 10;
airflow db init;

# Create 
airflow users create \
    --username airflow \
    --firstname airflow \
    --lastname admin \
    --role Admin \
    --email airflow@noreply.com;