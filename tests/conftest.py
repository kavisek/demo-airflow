"""Shared fixtures for smoke-testing a running Airflow deployment.

The tests talk to the Airflow REST API from the host. Configure them with:

- AIRFLOW_URL: base URL of the API server (default http://localhost:8080).
- AIRFLOW_USERNAME / AIRFLOW_PASSWORD: login (default airflow / airflow).
- EXPECTED_AIRFLOW_VERSION: if set, the deployed version must match it.
"""

import os
import time

import pytest
import requests

AIRFLOW_URL = os.environ.get("AIRFLOW_URL", "http://localhost:8080").rstrip("/")
USERNAME = os.environ.get("AIRFLOW_USERNAME", "airflow")
PASSWORD = os.environ.get("AIRFLOW_PASSWORD", "airflow")
READY_TIMEOUT = int(os.environ.get("AIRFLOW_READY_TIMEOUT", "600"))


def _wait_until_ready() -> None:
    deadline = time.monotonic() + READY_TIMEOUT
    last_error = None
    while time.monotonic() < deadline:
        try:
            response = requests.get(f"{AIRFLOW_URL}/api/v2/version", timeout=5)
            if response.ok:
                return
            last_error = f"HTTP {response.status_code}"
        except requests.RequestException as exc:
            last_error = exc
        time.sleep(5)
    pytest.exit(f"Airflow API at {AIRFLOW_URL} not ready after {READY_TIMEOUT}s: {last_error}")


@pytest.fixture(scope="session")
def api() -> requests.Session:
    """An authenticated session whose requests are relative to /api/v2."""
    _wait_until_ready()
    token = requests.post(
        f"{AIRFLOW_URL}/auth/token",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=10,
    )
    token.raise_for_status()

    session = _ApiSession(f"{AIRFLOW_URL}/api/v2")
    session.headers["Authorization"] = f"Bearer {token.json()['access_token']}"
    return session


class _ApiSession(requests.Session):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        kwargs.setdefault("timeout", 30)
        return super().request(method, f"{self.base_url}{url}", *args, **kwargs)
