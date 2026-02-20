import pytest

from utils.api_client import APIClient


@pytest.fixture(scope="session")
def browserstack_url():
    """Returns the BrowserStack endpoint with credentials"""
    # BrowserStack integration works out of the box when you set
    # BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY
    # and run with `browserstack-sdk pytest`
    # Default local playwright fixture will be used
    return None


@pytest.fixture(scope="session")
def api_client():
    """Returns an API client instance"""
    return APIClient()


@pytest.fixture
def page(context):
    """Overrides the default page fixture to help ensure clean states"""
    page = context.new_page()
    yield page
    page.close()
