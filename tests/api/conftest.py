import pytest

from utils.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    """Returns an API client instance"""
    return APIClient()
