
# List Connections
airflow connections list


# Setting up Airflow Connections

airflow connections add 'postgres_default' \
    --conn-json '{
        "conn_type": "postgres",
        "host": "postgres", 
        "port": 5432, 
        "schema": "postgres", 
        "login": "airflow", 
        "password": "airflow", 
        "extra": { "sslmode": "disable" }
    }'

airflow connections add \
    --conn_id postgres_default \
    --conn_type postgres \
    --conn_host postgres \
    --conn_login airflow \
    --conn_password airflow \
    --conn_schema postgres

# List Connections
airflow connections list

# Remove Connection
airflow connections delete postgres_default