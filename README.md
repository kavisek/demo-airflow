# Airflow demo with example DAGs

This repository runs Apache Airflow 3.3.2 on your machine with Docker Compose and includes a set of example DAGs. Use it to learn how Airflow works: after you follow this guide, you have a local Airflow deployment, you can run and inspect each example DAG, and you can check the deployment with an automated test suite.

## Overview

Apache Airflow is a workflow scheduler, like `cron` with dependencies, retries, and a web UI. You define pipelines as DAGs (directed acyclic graphs) of tasks in Python. Airflow runs them on a schedule and spreads the tasks across workers. Common uses are extract, transform, and load (ETL) jobs, model training, and any task that runs at a set frequency.

You can deploy Airflow in several ways:

| Option | Best for |
|---|---|
| Docker Compose | Local development. This repository uses it. |
| Kubernetes with the Airflow Helm chart | Production. See [Deploy on Kubernetes](#deploy-on-kubernetes). |
| A cloud virtual machine | Low-cost hosting. It's less stable, but cheaper than managed Airflow services, which can cost $1,000 or more per month. |

The Docker Compose deployment runs the following services:

- `airflow-apiserver`: the web UI and REST API.
- `airflow-scheduler`: schedules DAG runs and queues tasks.
- `airflow-dag-processor`: parses the files in `dags/`.
- `airflow-worker`: a Celery worker that runs tasks.
- `airflow-triggerer`: runs deferred tasks.
- `postgres`: the metadata database.
- `redis`: the Celery message broker.

The `docker-compose.yml` file is based on the [official Airflow Docker Compose file](https://airflow.apache.org/docs/apache-airflow/3.3.2/docker-compose.yaml). It differs in the following ways:

- The Airflow example DAGs are turned off, so you see only the DAGs in this repository.
- Authentication is turned off, so the UI and API don't ask for a login.
- New DAGs are unpaused when they're created, so scheduled DAGs start running right away.
- The host ports and secret keys are configurable. See [Configure the deployment](#configure-the-deployment).

> **Warning:** With authentication turned off, every request to the UI or API has admin access. Don't run this deployment on a machine or network that other people can reach.

## Before you begin

Install the following tools:

- [Docker](https://docs.docker.com/get-docker/), with at least 4 GB of memory and 2 CPUs for Docker.
- `make`.
- `openssl`, which generates the secret keys.
- [uv](https://docs.astral.sh/uv/), which runs the tests.
- `watch`, for the `make containers` command.

## Start Airflow

1. Clone the repository:

   ```sh
   git clone https://github.com/kavisek/demo-airflow.git
   cd demo-airflow
   ```

1. Start the deployment:

   ```sh
   make start
   ```

   On the first run, the command creates a `.env` file with new secret keys. It then migrates the metadata database and starts every service. The first start takes several minutes because each service installs the extra Python packages listed in `_PIP_ADDITIONAL_REQUIREMENTS`.

   When it finishes, the command prints the address of each service:

   ```text
   Airflow is starting up. Services on the host:
     Airflow UI / API: http://localhost:8080
                       no login needed (authentication is off)
     Postgres:         localhost:5432
                       username airflow, password airflow, database airflow
     Redis:            not published to the host (6379 inside the Docker network)
     Flower:           http://localhost:5555 (only with: docker compose --profile flower up -d)
   ```

1. Open the Airflow UI at `http://localhost:8080`.

   The `setup_dag` DAG runs once on its own and creates the `postgres_default` connection and the `environment` variable.

## Verify the deployment

1. Check that every service is running and healthy:

   ```sh
   docker compose ps --format 'table {{.Service}}\t{{.Status}}\t{{.Ports}}'
   ```

   The output is similar to the following:

   ```text
   SERVICE                 STATUS                   PORTS
   airflow-apiserver       Up 5 minutes (healthy)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
   airflow-dag-processor   Up 5 minutes (healthy)   8080/tcp
   airflow-scheduler       Up 5 minutes (healthy)   8080/tcp
   airflow-triggerer       Up 5 minutes (healthy)   8080/tcp
   airflow-worker          Up 5 minutes (healthy)   8080/tcp
   postgres                Up 5 minutes (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
   redis                   Up 5 minutes (healthy)   6379/tcp
   ```

   To watch the containers refresh every 2 seconds, run `make containers`.

1. Run the test suite:

   ```sh
   make test
   ```

   The tests in `tests/` call the REST API of the running deployment. They check the Airflow version and the health of each component, check that every DAG parses, trigger each DAG, and wait for each run to succeed. The output ends with a line similar to the following:

   ```text
   ============================= 25 passed in 38.63s ==============================
   ```

1. Optional: to also check the deployed Airflow version, set `EXPECTED_AIRFLOW_VERSION`:

   ```sh
   EXPECTED_AIRFLOW_VERSION=3.3.2 make test
   ```

## Explore the example DAGs

The `dags/` folder contains the following DAGs. Unless noted, each DAG runs daily at 00:00 UTC.

| DAG ID | What it shows |
|---|---|
| `bash_dag` | Bash commands with `BashOperator`, including a task that exits with code 99 to skip itself. |
| `branching_dag` | Choosing one of four branches at random with `BranchPythonOperator`. |
| `datetime_dag` | Branching on the time of day with `BranchDateTimeOperator`. |
| `dynamic_generated_dag_config1` to `dynamic_generated_dag_config4` | Generating four DAGs from one file. These DAGs have no schedule. |
| `global_variables_dag` | Reading the `environment` Airflow variable, which `docker-compose.yml` sets. |
| `module_dag` | Importing task code from a local Python module in `dags/module/`. |
| `pip_dag` | Printing the installed pip packages and the Python path. |
| `postgres_dag` | Creating a Postgres table, inserting a row, and reading it back. |
| `python_dag` | Running a Python function with `PythonOperator`. |
| `random_dependency` | A random number of parallel tasks, from 2 to 5, chosen each time the file is parsed. |
| `setup_dag` | Creating a connection and a variable through the REST API. Runs once. |
| `template_dag` | Generating cleaning and processing tasks for five countries in a loop. |
| `xcom_dag` | Passing a value between tasks with XCom. |

The following examples aren't available yet:

- `sensor_dag` and `sensor_trigger_dag`, which wait on another DAG with `ExternalTaskSensor`. The code is commented out.
- A DAG factory that builds DAGs from YAML. The code in `dags/config_factory/` is commented out.
- A DAG on a custom external schedule, and a DAG with a service level agreement (SLA). These are planned.

## Configure the deployment

### Change the host ports

The API server uses port 8080 and Postgres uses port 5432 on your machine. If another program already uses either port, set different ports before you run `make start` and `make test`:

```sh
export AIRFLOW_API_PORT=API_PORT POSTGRES_PORT=POSTGRES_PORT
make start
make test
```

Replace the following:

- `API_PORT`: a free port for the Airflow UI and API, for example `8090`.
- `POSTGRES_PORT`: a free port for Postgres, for example `5442`.

### Manage secret keys

The first `make start` creates a `.env` file with a new Fernet key, API secret key, and JSON Web Token (JWT) secret. Git ignores `.env`, and each clone gets its own keys. The `.env.example` file lists the variables. To use your own values, create `.env` before you run `make start`.

The Fernet key encrypts connection passwords and variables in the metadata database. If you change it, Airflow can't decrypt the values it already stored. See [Connections page returns an error](#connections-page-returns-an-error).

## Run common tasks

To follow the scheduler logs, run the following command:

```sh
docker compose logs -f airflow-scheduler
```

To open a shell in the scheduler container, run the following command:

```sh
docker compose exec airflow-scheduler bash
```

To create runs for past dates, use a backfill. The following command shows the runs it would create without creating them:

```sh
docker compose exec airflow-scheduler \
  airflow backfill create --dag-id DAG_ID --from-date START_DATE --to-date END_DATE --dry-run
```

Replace the following:

- `DAG_ID`: the DAG to backfill, for example `python_dag`.
- `START_DATE` and `END_DATE`: the first and last dates of the range, for example `2026-10-01` and `2026-10-03`.

To create the runs, run the command again without `--dry-run`. For more information, see [Backfill](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html) in the Airflow documentation.

## Clean up

To stop and remove the containers, run the following command:

```sh
make stop
```

The metadata database is kept in the `demo-airflow_postgres-db-volume` Docker volume, so your DAG run history is still there the next time you run `make start`.

> **Caution:** The following command deletes the metadata database, including all DAG run history, connections, and variables.

To remove the containers and the database, run the following command:

```sh
docker compose down -v
```

## Troubleshoot

### Port is already allocated

If `make start` fails with `port is already allocated`, another program is using port 8080 or 5432. Choose other ports as described in [Change the host ports](#change-the-host-ports).

### Connections page returns an error

If the **Connections** page or the `/api/v2/connections` endpoint returns an error, the database holds values encrypted with a different Fernet key. This happens if `.env` changed, or if the database was created by an older checkout of this repository, which had fixed keys. The `test_stored_secrets_decrypt` test fails in this case.

To start over with an empty database, run the following commands:

```sh
docker compose down -v
make start
```

## Deploy on Kubernetes

You can also deploy Airflow with the [Airflow Helm chart](https://airflow.apache.org/docs/helm-chart/stable/index.html):

```sh
kubectl create namespace airflow
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  --set webserver.livenessProbe.initialDelaySeconds=30
```

To watch the pods start, run the following command:

```sh
watch -n 30 kubectl get namespace,deployment,svc,po -A
```

## What's next

With the deployment running, you can try the following:

- Write your own DAGs in `dags/`. The DAG processor picks up new files automatically.
- Install plugins in `plugins/`.
- Add connections in the UI under **Admin** > **Connections**.
- Monitor DAG runs and task logs in the UI.

To learn more, see the following resources:

- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [Airflow documentation](https://airflow.apache.org/)
- [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Postgres connection](https://airflow.apache.org/howto/connection/postgres.html)
- [Airflow Helm chart source](https://github.com/apache/airflow/tree/master/chart)
- [Airflow Breeze development environment](https://github.com/apache/airflow/blob/master/BREEZE.rst)
- [Run PostgreSQL in Docker on a Mac for local development](https://www.saltycrane.com/blog/2019/01/how-run-postgresql-docker-mac-local-development///)

## Contributing

Contributions are welcome. For setup and the pull request process, see [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). To report a security problem, follow [SECURITY.md](SECURITY.md).

## License

This project is licensed under the [MIT License](LICENSE).
