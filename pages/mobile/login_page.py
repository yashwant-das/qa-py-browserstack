from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from pages.mobile.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the WDIO Sample App Login screen."""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # We determine the platform from the driver capabilities
        self.platform = driver.capabilities.get("platformName", "").lower()

        self.locators = {
            "login_tab": {
                "android": (AppiumBy.ACCESSIBILITY_ID, "Login"),
                "ios": (AppiumBy.ACCESSIBILITY_ID, "Login"),
            },
            "email_input": {
                "android": (AppiumBy.ACCESSIBILITY_ID, "input-email"),
                "ios": (AppiumBy.ACCESSIBILITY_ID, "input-email"),
            },
            "password_input": {
                "android": (AppiumBy.ACCESSIBILITY_ID, "input-password"),
                "ios": (AppiumBy.ACCESSIBILITY_ID, "input-password"),
            },
            "login_button": {
                "android": (AppiumBy.ACCESSIBILITY_ID, "button-LOGIN"),
                "ios": (AppiumBy.ACCESSIBILITY_ID, "button-LOGIN"),
            },
            "success_message_title": {
                "android": (AppiumBy.ID, "android:id/alertTitle"),
                "ios": (AppiumBy.ACCESSIBILITY_ID, "Success"),
            },
            "success_message_text": {
                "android": (AppiumBy.ID, "android:id/message"),
                "ios": (AppiumBy.ACCESSIBILITY_ID, "You are logged in!"),
            },
        }

    def _get_locator(self, locator_name: str) -> tuple[str, str]:
        """Helper method to dynamically fetch the correct locator based on OS."""
        locator_dict = self.locators.get(locator_name)
        if not locator_dict:
            raise ValueError(
                f"Locator '{locator_name}' not defined in {self.__class__.__name__}"
            )

        locator = locator_dict.get(self.platform)
        if not locator:
            return locator_dict.get("android")
        return locator

    def go_to_login_tab(self) -> None:
        """Click the Login tab in the bottom navigation."""
        self.click(self._get_locator("login_tab"))

    def login(self, email: str, password: str) -> None:
        """Perform login action."""
        self.input_text(self._get_locator("email_input"), email)
        self.input_text(self._get_locator("password_input"), password)
        self.click(self._get_locator("login_button"))

    def get_success_message(self) -> str:
        """Fetch the success message text from the alert."""
        if self.platform == "ios":
            # In iOS, often the alert text is accessible by its value/name directly
            # Let's verify both title and text are displayed
            title_displayed = self.is_displayed(
                self._get_locator("success_message_title")
            )
            text_displayed = self.is_displayed(
                self._get_locator("success_message_text")
            )
            if title_displayed and text_displayed:
                return "You are logged in!"
            return "Failed to find success message on iOS"
        else:
            # Android
            return self.get_text(self._get_locator("success_message_text"))
