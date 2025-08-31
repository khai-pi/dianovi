# conftest.py
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add current directory to path BEFORE importing main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def valid_login_data():
    return {"username": "doctor", "password": "password"}


@pytest.fixture
def invalid_login_data():
    return {"username": "wrong", "password": "wrong"}
