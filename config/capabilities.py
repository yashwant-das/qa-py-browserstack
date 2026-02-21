import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Local capabilities for Android and iOS simulators
LOCAL_CAPS = {
    "android": {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Medium Phone API 36.1",
        "appium:platformVersion": "16.0",
        "appium:appPackage": "com.wdiodemoapp",
        "appium:appActivity": ".MainActivity",
        "appium:autoGrantPermissions": True,
        "appium:enforceAppInstall": True,
        "appium:noReset": False,
        "appium:app": os.path.join(
            PROJECT_ROOT, "apps", "android", "android.wdio.native.app.v2.0.0.apk"
        ),
    },
    "ios": {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        # Note: Omitting `appium:udid` allows tests to run on the configured device below,
        # but Appium's fuzzy matching may occasionally boot a "ghost" simulator
        # (like iPhone 17 Pro Max) in the background during session initialization.
        # This is a known local Appium behavior when similar simulators exist on the host.
        "appium:deviceName": "iPhone 17 Pro",
        "appium:platformVersion": "26.2",
        "appium:app": os.path.join(
            PROJECT_ROOT, "apps", "ios", "ios.simulator.wdio.native.app.v2.0.0.zip"
        ),
    },
}


def get_local_caps(platform: str) -> dict:
    """Return the local capabilities for the requested platform."""
    caps = LOCAL_CAPS.get(platform.lower())
    if not caps:
        raise ValueError(f"No local capabilities defined for platform: {platform}")
    return caps
