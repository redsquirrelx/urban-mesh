import pytest
from fastapi.testclient import TestClient
from urbanmesh.bootstrap import build_services
from urbanmesh.presentation.api import create_app

@pytest.fixture
def services(): return build_services()

@pytest.fixture
def client(services):
    with TestClient(create_app(services)) as api:
        yield api
