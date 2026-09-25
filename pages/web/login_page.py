from pages.web.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'
    INVENTORY_CONTAINER = ".inventory_container"

    def __init__(self, page):
        super().__init__(page)

    def navigate_to_login(self, base_url="https://www.saucedemo.com/"):
        self.navigate(base_url)

    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_logged_in(self) -> bool:
        return self.wait_until_visible(self.INVENTORY_CONTAINER)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
