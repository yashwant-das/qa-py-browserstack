from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class for all Page Objects in the Mobile App"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find_element(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        """Wait for an element to be present and return it."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found after {timeout} seconds.")

    def click(self, locator: tuple[str, str], timeout: int = 10) -> None:
        """Wait for an element to be clickable and click it."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable after {timeout} seconds.")

    def input_text(self, locator: tuple[str, str], text: str, timeout: int = 10) -> None:
        """Wait for an element to be present, clear it, and input text."""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def is_displayed(self, locator: tuple[str, str], timeout: int = 5) -> bool:
        """Check if an element is currently displayed on the screen."""
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except TimeoutException:
            return False

    def get_text(self, locator: tuple[str, str], timeout: int = 10) -> str:
        """Get the visible text of an element."""
        return self.find_element(locator, timeout).text
