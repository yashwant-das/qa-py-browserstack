from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the Wikipedia Sample App Login/Search screen."""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # We determine the platform from the driver capabilities
        self.platform = driver.capabilities.get("platformName", "").lower()

        # Define locators as dictionaries holding both iOS and Android selectors
        # For this POC, we are using the Wikipedia Sample App from Browserstack

        self.locators = {
            "search_input": {
                "android": (AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"),
                "ios": (AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"),
            },
            "search_box": {
                "android": (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"),
                "ios": (
                    AppiumBy.ACCESSIBILITY_ID,
                    "Search Wikipedia",
                ),  # Simplified for iOS POC
            },
            "search_results": {
                "android": (AppiumBy.CLASS_NAME, "android.widget.TextView"),
                "ios": (AppiumBy.XCUI_ELEMENT_TYPE, "XCUIElementTypeStaticText"),
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
            # Fallback to Android if platform mapping is missing, or raise error
            return locator_dict.get("android")
        return locator

    def perform_search(self, keyword: str) -> None:
        """Search Wikipedia using the app."""
        self.click(self._get_locator("search_input"))
        self.input_text(self._get_locator("search_box"), keyword)

    def get_search_results(self) -> list:
        """Fetch the text of all search results on screen."""
        locator = self._get_locator("search_results")
        # BasePage doesn't have a find_elements (plural) yet, so we use driver directly here
        # or we could add find_elements to BasePage.
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(locator)
        )
        return [el.text for el in elements]
