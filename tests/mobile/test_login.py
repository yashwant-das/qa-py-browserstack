from pytest_testrail.plugin import pytestrail

from pages.login_page import LoginPage


class TestDemoApp:
    @pytestrail.case("47")
    def test_login_success(self, driver):
        """
        Test that login with valid credentials yields success message.
        Runs dynamically on whatever platform BrowserStack routes to, or locally.
        """
        page = LoginPage(driver)

        # 1. Navigate to Login Tab
        page.go_to_login_tab()

        # 2. Enter credentials and login
        page.login("test@gmail.com", "12345678")

        # 3. Verify success message
        success_msg = page.get_success_message()

        assert "You are logged in!" in success_msg, (
            f"Expected success message not found. Got: {success_msg}"
        )
