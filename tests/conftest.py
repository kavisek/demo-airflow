"""Shared fixtures for smoke-testing a running Airflow deployment.

The tests talk to the Airflow REST API from the host. Configure them with:

- AIRFLOW_URL: base URL of the API server (default http://localhost:8080).
- EXPECTED_AIRFLOW_VERSION: if set, the deployed version must match it.
"""

import os
import time

import pytest
import requests

AIRFLOW_URL = os.environ.get("AIRFLOW_URL", "http://localhost:8080").rstrip("/")
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
    """A session whose requests are relative to /api/v2.

    Authentication is turned off in docker-compose.yml, so no token is needed.
    """
    _wait_until_ready()
    return _ApiSession(f"{AIRFLOW_URL}/api/v2")


class _ApiSession(requests.Session):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        kwargs.setdefault("timeout", 30)
        return super().request(method, f"{self.base_url}{url}", *args, **kwargs)
