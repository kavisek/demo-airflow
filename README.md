# Airflow-DAGs

Apache Airflow is a like a crontab on steroids. Its a pipeline framework that can be used for ETL processing and model training if your are dealing with very large complex setups. The framework allows you to run multiple jobs across different workers. I have a simple implementation of Airflow running on my local machine. If you want to set up an instance on your local machine use the small tutorial found below

This repo contains some useful DAGs (dynamic acyclic graphs) in Python that I use to automate my workflow. Feel free to modify these DAGs to your use case.

### DAG Descriptions

- **train_models.py** - Run notebooks and the model within them overnight every night
- **update_blog.py** - Run a python script that generates the content for my blog overnight
- **update_logs.py** - Output a log every hours to makes sure the Airflow Scheduler is working

### Local Airflow Setup Instructions

1. Create a virtual environment using conda.

`conda create --name airflow`

2. Activate and enter your new virtual environment

`source activate airflow`

2. Conda Install Airflow into the "airflow" environment

`conda install -c conda-forge airflow`

4. Start the Airflow web server.

`airflow webserver -p 8080`

5. Start the Airflow scheduler

`airflow scheduler`

6. Visit "http://localhost:8080/admin/" to view the Airflow Dashboard to run your DAGs

![Image](./Images/local_airflow.png)

### General Notes

As I learn more through threw my experimentation. I will be adding to these notes below.

- You can modify Airflow paths and DAG locations in the Airflow config file.
- If you are running bash script using the Bash Operator place an extra space at the end of the Python script.
- If you modify or add a DAG to Airflow, it can take up to 5 minutes so show up in the web server.
- If you change the name of a DAG, unlink the DAG in Airflow before renaming it within the Python file.


### Sources

- [Airflow Documentation](https://airflow.apache.org/)
