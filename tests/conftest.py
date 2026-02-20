import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from utils.jira_client import JiraClient

# Global instance
jira_client = JiraClient()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Check if the --jira flag was passed
    jira_enabled = item.config.getoption("--jira")

    # We only look at actual test calls, not setup/teardown
    if report.when == "call" and report.failed and jira_enabled:
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


def pytest_addoption(parser):
    """Add custom command line arguments"""
    parser.addoption(
        "--jira",
        action="store_true",
        default=False,
        help="Create/Update Jira defects automatically on test failures",
    )
    # Local Appium execution arguments
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Platform to run tests on locally (android or ios)",
    )
    parser.addoption(
        "--app-path",
        action="store",
        default="",
        help="Absolute path to the local .apk or .ipa file for Appium",
    )
    parser.addoption(
        "--device-name",
        action="store",
        default="",
        help="Specific local device or emulator name (e.g. emulator-5554 or 'iPhone 15 Simulator')",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Appium driver setup.
    When run locally without Browserstack SDK, it uses custom CLI options.
    assuming Appium is running on http://127.0.0.1:4723
    """
    appium_server_url = "http://127.0.0.1:4723"

    # Are we running on BrowserStack or Locally?
    # BrowserStack SDK injects capabilities implicitly, so an empty Options object suffices.
    # If running locally, we need to manually construct the capabilities using the CLI flags.
    is_browserstack = bool(os.getenv("BROWSERSTACK_USERNAME"))

    platform = request.config.getoption("--platform").lower()
    app_path = request.config.getoption("--app-path")
    device_name = request.config.getoption("--device-name")

    if platform == "ios":
        options = XCUITestOptions()
        if not is_browserstack:
            options.platform_name = "iOS"
            options.automation_name = "XCUITest"
    else:
        options = UiAutomator2Options()
        if not is_browserstack:
            options.platform_name = "Android"
            options.automation_name = "UiAutomator2"

    if not is_browserstack:
        if app_path:
            options.app = os.path.abspath(app_path)
        if device_name:
            options.device_name = device_name

        print(
            f"\n[LOCAL EXECUTION] Launching on {platform} with {options.to_capabilities()}"
        )

    # The BS SDK will inject its own URL and Caps over these if running via `browserstack-sdk pytest`
    driver = webdriver.Remote(appium_server_url, options=options)

    yield driver

    driver.quit()
