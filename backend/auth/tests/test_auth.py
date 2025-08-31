# test_auth.py

import sys
import os

# import pytest
# from fastapi import HTTPException, status
# from fastapi.testclient import TestClient

# import jwt
# from unittest.mock import patch, MagicMock

# Add parent directory to path to import your main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_login_success(client, valid_login_data):
    """Test successful login"""
    response = client.post("/api/login", json=valid_login_data)
    assert response.status_code == 200


def test_login_failure(client, invalid_login_data):
    """Test failed login"""
    response = client.post("/api/login", json=invalid_login_data)
    assert response.status_code == 401
