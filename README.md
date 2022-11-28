# Airflow and DAGs

This repo review how to run Airflow locally with a few examples of DAGs 

In General, Apache Airflow is a like a crontab on steroids. Its a pipeline framework that can be used for ETL processing, training models, or any task that needs to be run at certain frequency. The framework allows you to run multiple jobs across different workers and specify dependencies. 

There are few options on how to deploy Airflow.

docker-compose: great for local development
kubernetes / helm: best for a production use case
Cloud Virtual Machine: Not the stable but a very cheap alternative to most $1000 per month options.

# Docker Startup

I use `Makefile` a lot in my code to consolidate most of the docker-compose commands your need to run.  The following make command will provision the database, webserver, and scheduler locally for you. 


## Dependencies

- make
- watch
- docker

## Quick Start

The docker compose file for this quickstart is very similar to what is provided by the airflow team. I have made the following modifications

- added a volume mount for the script directory.

```bash
# Start docker-compose via Makefile command.
make startup
```

The above command set up the postgres meta-datbase, webserver, scheduler, and workers. It may take a few moments for everything to initialize.

Visit http://localhost:8080/ to interact with the webserver and the sample dags.

username: airflow  
password: airflow

![WebServer](/images/webserver.png)

You can view running containers after startup.

```bash
# view the running containers
make containers
```

![Containers](/images/running_containers.png)


### DAG Samples

I remove all template example dags from Airflow local deployment, and loaded my own examples. 

These are dags that I have written using best practises.

- python_operator: A dag that run python script.
- bash_dag: A dag that run bash script.
- branch_dag: A dag that branch based on a task output.
- datetime_dag: A dag that branch based on time.
- postgres_dag: A dag that loads data into postgres.
- custom_schedule_dag: A dag that runs on a predefined external schedule. (pending)
- dag_factory_dag: An example of a dag factory using yaml.
- templated dag: A dag that is template over multiple office locations.
- sla_dag: A dag with a defined SLA. (pending)
- sensor_dag: A dag that uses task sensors
- xcom_dag: A dag that use xcom to pass variables.
- pip_dag: A dag that export airflow pip requirements and sys paths (sneaky).


### Backfilling Commads

```
# View Scheduler Logs
docker logs airflow-dags-airflow-scheduler-1

# Bash into Airflow scheduler
docker exec -it airflow-dags-airflow-webserver-1 /bin/bash

# Backfill 

```


### Airflow Best Practises

### Experimentation

You can now play around with Airflow features in a local environment.

- Build DAGs
- Install Plugins
- Setup Connections
- Monitor Jobs

## Kubernetes Startup

This setup is using the [Airflow Helm distribution for Kubernetes](https://airflow.apache.org/docs/helm-chart/stable/index.html).

```bash
# Create airflow namespace
kubectl create namespace airflow

# Adding repo
helm repo add apache-airflow https://airflow.apache.org

# Install helm chart.
kubectl create namespace airflow
helm install airflow apache-airflow/airflow \
--namespace airflow \
--set webserver.livenessProbe.initialDelaySeconds=30
```

If you would like to monitor the distribution of the pods. Feel free to check out this watch and kubectl for active in-terminal monitoring.

```bash
watch -n 30 kubectl get namespace,deployment,svc,po -A
```

<br></br><center>
![Airflow Diagram](https://www.xenonstack.com/images/insights/xenonstack-what-is-apache-airflow.png)

### Sources

- [Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [Airflow Helm](https://github.com/apache/airflow/tree/master/chart)
- [Airflow in Breeze](https://github.com/apache/airflow/blob/master/BREEZE.rst)
- [Airflow Documentation](https://airflow.apache.org/)
- [Postgres Docker Container Setup](https://www.saltycrane.com/blog/2019/01/how-run-postgresql-docker-mac-local-development///)
- [Postgres Connection String](https://airflow.apache.org/howto/connection/postgres.html)
- [Installing Helm Chart](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/helm-chart/latest/index.html)
- [Airflow Docker Compose](https://airflow.apache.org/docs/apache-airflow/2.4.3/docker-compose.yaml)