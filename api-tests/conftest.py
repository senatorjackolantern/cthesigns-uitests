import os
import pytest
import requests

DEFAULT_API_BASE_URL = "https://ng12assessor.fanai.dev" 

@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")

@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({
        "Accept": "application/json",
    })
    yield s
    s.close()