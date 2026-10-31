# Contributing to demo-airflow

Thanks for your interest in contributing! This repo is a set of example Airflow DAGs and a local Docker Compose deployment for trying them out.

## Development setup

You need Docker, `make`, `openssl`, and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/kavisek/demo-airflow.git
cd demo-airflow
uv sync
make start      # first run generates .env with fresh secret keys
```

Airflow is then at http://localhost:8080. If port 8080 or 5432 is taken, set `AIRFLOW_API_PORT` or `POSTGRES_PORT` first (see the README).

## Running tests

The tests smoke-test the running deployment through the REST API, so start it first:

```sh
make start
make test
make stop
```

## Adding a DAG

1. Put it in its own folder under `dags/`, for example `dags/my_example/my_example_dag.py`.
2. Add its `dag_id` to `EXPECTED_DAGS` in `tests/test_dags.py` so the tests check that it parses and runs.
3. Keep it self-contained: it should run on the demo stack with no extra setup or credentials.

## Making a change

1. Open an issue first for anything bigger than a small fix, so we can agree on the approach.
2. Fork the repo and create a branch: `git switch -c feat/my-change`.
3. Write commits in [Conventional Commits](https://www.conventionalcommits.org/) style (`feat:`, `fix:`, `docs:`, `chore:`).
4. Add or update tests, and make sure `make test` passes.
5. Open a pull request against `main` and fill in the template.

Never commit `.env` or any real credentials.

## Code of conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## License

By contributing, you agree that your contributions are licensed under the project's [license](LICENSE).
