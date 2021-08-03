# Airflow and DAGs

A repo that explores implementing airflow locally using container via docker-compose and kubernetes. This is a good template to build on, and customize your own container solution.

In General, Apache Airflow is a like a crontab on steroids. Its a pipeline framework that can be used for ETL processing, training model overnight, or any task that needs to be run at certain frequency. The framework allows you to run multiple jobs across different workers. I have a simple implementation of Airflow running on my local machine with the airflow server using docker containers. Therefore you run this near production example on your local machine using docker container and then migrate to Amazon Web Services or the Google Cloud Platform.

<br></br><center>
![Airflow Diagram](https://www.xenonstack.com/images/insights/xenonstack-what-is-apache-airflow.png)

</center>

# Docker Startup

You review the make file to view the commands to initialize the database and run the scheduler and webserver. This following command will do everything for you.

```bash
# Start docker via Makefile command.
make startup
```

The above command set up the postgres meta-datbase, webserver, scheduler, and workers.

Visit http://localhost:8080/ to interact with the webserver and the sample dags.

![WebServer](/images/webserver.png)

Username: airflow  
Password: airflow

You can view running containers after startup.

```bash
# view the running containers
docker containers ls
```

![Containers](/images/running_containers.png)

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


### Sources

- [Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [Airflow Helm](https://github.com/apache/airflow/tree/master/chart)
- [Airflow in Breeze](https://github.com/apache/airflow/blob/master/BREEZE.rst)
- [Airflow Documentation](https://airflow.apache.org/)
- [Postgres Docker Container Setup](https://www.saltycrane.com/blog/2019/01/how-run-postgresql-docker-mac-local-development///)
- [Postgres Connection String](https://airflow.apache.org/howto/connection/postgres.html)
- [Installing Helm Chart](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/helm-chart/latest/index.html)
