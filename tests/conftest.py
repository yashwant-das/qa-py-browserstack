import pytest

from utils.api_client import APIClient
from utils.jira_client import JiraClient

# Global instance
jira_client = JiraClient()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # We only look at actual test calls, not setup/teardown
    if report.when == "call" and report.failed:
        # Extract the node ID (test name)
        test_name = item.nodeid

        # Safely extract error traceback
        error_message = "Test execution failed."
        traceback_details = ""

        if hasattr(report.longrepr, "reprcrash"):
            error_message = report.longrepr.reprcrash.message

        if report.longreprtext:
            traceback_details = report.longreprtext

        print(f"\n[JIRA HOOK] Detected failure for {test_name}. Notifying Jira...")
        issue_key = jira_client.create_or_update_defect(
            test_name=test_name,
            error_message=error_message,
            traceback=traceback_details,
        )
        if issue_key:
            print(f"[JIRA HOOK] Successfully processed Jira Ticket: {issue_key}")


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
