import pytest

from utils.jira_client import JiraClient

_jira_client = None


def _jira():
    global _jira_client
    if _jira_client is None:
        _jira_client = JiraClient()
    return _jira_client


def pytest_addoption(parser):
    """Options for every suite. pytest only reads pytest_addoption from the root conftest."""
    parser.addoption(
        "--jira",
        action="store_true",
        default=False,
        help="Create/Update Jira defects automatically on test failures",
    )
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Mobile platform to run on locally (android or ios)",
    )
    parser.addoption(
        "--app-path",
        action="store",
        default="",
        help="Path to a local .apk or .ipa file for Appium",
    )
    parser.addoption(
        "--device-name",
        action="store",
        default="",
        help="Local device or emulator name (e.g. emulator-5554 or 'iPhone 15 Simulator')",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed or not item.config.getoption("--jira"):
        return

    test_name = item.nodeid
    error_message = "Test execution failed."
    if hasattr(report.longrepr, "reprcrash"):
        error_message = report.longrepr.reprcrash.message
    traceback_details = report.longreprtext or ""

    print(f"\n[JIRA HOOK] Detected failure for {test_name}. Notifying Jira...")
    issue_key = _jira().create_or_update_defect(
        test_name=test_name,
        error_message=error_message,
        traceback=traceback_details,
    )
    if issue_key:
        print(f"[JIRA HOOK] Successfully processed Jira Ticket: {issue_key}")
