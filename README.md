# Airflow-DAGs

Apache Airflow is a like crontab on steroids. Its a pipeline framework that can me used for ETL processing and model training if your are dealing with very large values. The framework allows your to run multiple jobs across different workers with dependancies. I have a simple implementation of Airflow running on my local machine. If you want to set up an instance on your local machine use these few commands.

1. Create a virtual enviroment using conda.

`conda create --name airflow`

2. Activate and enter your new virtual enviroment

`source activate airflow`

2. Conda Install Airflow into the "airflow" enviroment

`conda install -c conda-forge airflow`

4. Start the Airflow webserver.

`airflow webserver -p 8080`

5. Start the Airflow scheduler

`airflow scheduler`

6. Visit "http://localhost:8080/admin/" to view the Airflow Dashboard to run your DAGs

![Image](./Images/local_airflow.png)

### General Notes

As I learn more through threw my experimentation. I will be adding to these notes below.

- You can modify Airflow paths and DAG locations in the Airflow config file.
- If you are running bash script using the Bash Operator place an extra space at the end of the Python script
