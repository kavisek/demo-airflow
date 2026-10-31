"""The deployment is up, on the expected version, and every component is healthy."""

import os

import pytest
import requests

COMPONENTS = ["metadatabase", "scheduler", "triggerer", "dag_processor"]


def test_version(api):
    response = api.get("/version")
    response.raise_for_status()
    version = response.json()["version"]
    print(f"Airflow version: {version}")

    expected = os.environ.get("EXPECTED_AIRFLOW_VERSION")
    if expected:
        assert version == expected


@pytest.mark.parametrize("component", COMPONENTS)
def test_component_healthy(api, component):
    response = api.get("/monitor/health")
    response.raise_for_status()
    assert response.json()[component]["status"] == "healthy"




def test_api_needs_no_login():
    # docker-compose.yml turns authentication off for this demo.
    from conftest import AIRFLOW_URL

    response = requests.get(f"{AIRFLOW_URL}/api/v2/dags", timeout=30)
    assert response.status_code == 200
