"""Every demo DAG parses, and the runnable ones finish successfully."""

import time

import pytest

# DAG ids defined under dags/. sensor_dag, sensor_trigger_dag and config_dag are
# commented out in the repo, so they are not expected.
EXPECTED_DAGS = {
    "bash_dag",
    "branching_dag",
    "datetime_dag",
    "dynamic_generated_dag_config1",
    "dynamic_generated_dag_config2",
    "dynamic_generated_dag_config3",
    "dynamic_generated_dag_config4",
    "global_variables_dag",
    "module_dag",
    "pip_dag",
    "postgres_dag",
    "python_dag",
    "random_dependency",
    "setup_dag",
    "template_dag",
    "xcom_dag",
}

# DAGs to trigger end to end. All of them run on the demo stack with no extra setup.
RUN_DAGS = sorted(EXPECTED_DAGS)

RUN_TIMEOUT = 600
FINISHED = {"success", "failed"}


def _all_dag_ids(api) -> set[str]:
    dag_ids, offset = set(), 0
    while True:
        response = api.get("/dags", params={"limit": 100, "offset": offset})
        response.raise_for_status()
        page = response.json()["dags"]
        dag_ids |= {dag["dag_id"] for dag in page}
        if len(page) < 100:
            return dag_ids
        offset += 100


def test_no_import_errors(api):
    response = api.get("/importErrors")
    response.raise_for_status()
    errors = response.json()["import_errors"]
    assert errors == [], "\n\n".join(f"{e['filename']}:\n{e['stack_trace']}" for e in errors)


def test_expected_dags_registered(api):
    deadline = time.monotonic() + 120
    while (missing := EXPECTED_DAGS - _all_dag_ids(api)) and time.monotonic() < deadline:
        time.sleep(5)  # The DAG processor may still be parsing on a fresh start.
    assert not missing, f"DAGs not registered: {sorted(missing)}"


@pytest.fixture(scope="module")
def dag_runs(api):
    """Trigger every DAG in RUN_DAGS once and wait for all runs to finish.

    Returns {dag_id: (state, failed_task_ids)}. Each DAG is put back to its
    original paused state afterwards.
    """
    paused = {}
    run_ids = {}
    for dag_id in RUN_DAGS:
        dag = api.get(f"/dags/{dag_id}")
        dag.raise_for_status()
        paused[dag_id] = dag.json()["is_paused"]
        api.patch(f"/dags/{dag_id}", json={"is_paused": False}).raise_for_status()

        run = api.post(f"/dags/{dag_id}/dagRuns", json={"logical_date": None})
        run.raise_for_status()
        run_ids[dag_id] = run.json()["dag_run_id"]

    results = {}
    deadline = time.monotonic() + RUN_TIMEOUT
    while len(results) < len(run_ids) and time.monotonic() < deadline:
        for dag_id, run_id in run_ids.items():
            if dag_id in results:
                continue
            run = api.get(f"/dags/{dag_id}/dagRuns/{run_id}")
            run.raise_for_status()
            state = run.json()["state"]
            if state in FINISHED:
                tasks = api.get(f"/dags/{dag_id}/dagRuns/{run_id}/taskInstances")
                tasks.raise_for_status()
                failed = sorted(
                    t["task_id"]
                    for t in tasks.json()["task_instances"]
                    if t["state"] in {"failed", "upstream_failed"}
                )
                results[dag_id] = (state, failed)
        time.sleep(5)

    for dag_id, was_paused in paused.items():
        api.patch(f"/dags/{dag_id}", json={"is_paused": was_paused})

    for dag_id in run_ids:
        results.setdefault(dag_id, ("timed out", []))
    return results


@pytest.mark.parametrize("dag_id", RUN_DAGS)
def test_dag_run_succeeds(dag_runs, dag_id):
    state, failed_tasks = dag_runs[dag_id]
    assert state == "success", f"{dag_id} finished as {state}; failed tasks: {failed_tasks}"
