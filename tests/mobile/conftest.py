import os
import sys

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from config.mobile_capabilities import get_local_caps


@pytest.fixture(scope="function")
def driver(request):
    """
    Appium driver setup.
    When run locally without Browserstack SDK, it uses custom CLI options.
    assuming Appium is running on http://127.0.0.1:4723
    """
    appium_server_url = "http://127.0.0.1:4723"

    # Are we running on BrowserStack or Locally?
    # When running via `browserstack-sdk pytest`, the SDK binary is the entry point (sys.argv[0]).
    # The browserstack_sdk plugin is usually disabled in pytest.ini to avoid local conflicts,
    # but the SDK CLI forces it in.
    is_browserstack = (
        "browserstack-sdk" in sys.argv[0]
        or request.config.pluginmanager.hasplugin("browserstack_sdk")
        or os.getenv("BROWSERSTACK_SDK") == "true"
        or os.getenv("BROWSERSTACK_AUTOMATION") == "true"
        or os.getenv("GITHUB_ACTIONS") == "true"
    )

    platform = request.config.getoption("--platform").lower()
    app_path = request.config.getoption("--app-path")
    device_name = request.config.getoption("--device-name")

    if is_browserstack:
        # On BrowserStack, the SDK handles platform selection and capabilities via browserstack.yml
        # We just need a generic options object to satisfy the driver initialization
        from appium.options.common import AppiumOptions

        options = AppiumOptions()
    elif platform == "ios":
        options = XCUITestOptions()
    else:
        options = UiAutomator2Options()

    if not is_browserstack:
        # Load default local capabilities from config
        local_caps = get_local_caps(platform)
        options.load_capabilities(local_caps)

        # Override with explicit CLI flags if provided
        if app_path:
            options.app = os.path.abspath(app_path)
        if device_name:
            options.device_name = device_name

    # The BS SDK will inject its own URL and Caps over these if running via `browserstack-sdk pytest`
    driver = webdriver.Remote(appium_server_url, options=options)

    yield driver

    driver.quit()
