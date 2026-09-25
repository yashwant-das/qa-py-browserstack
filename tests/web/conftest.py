import pytest


@pytest.fixture
def page(context):
    """Overrides the default page fixture to help ensure clean states"""
    page = context.new_page()
    yield page
    page.close()
