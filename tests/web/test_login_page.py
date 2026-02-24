from playwright.sync_api import expect
from pytest_testrail.plugin import pytestrail

from pages.login_page import LoginPage


@pytestrail.case("46")
def test_successful_login(page):
    """Test valid login functionality on SauceDemo"""
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    # breakpoint()
    # page.pause()
    login_page.login("standard_user", "secret_sauce")

    # Assert successful login by checking inventory is visible
    assert login_page.is_logged_in(), "Inventory container not visible after login"
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_invalid_login(page):
    """Test invalid login credentials on SauceDemo"""
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login("locked_out_user", "secret_sauce")

    # Assert specific error message appears
    assert not login_page.is_logged_in(), "Inventory should not be visible"
    error_message = login_page.get_error_message()
    assert "Epic sadface: Sorry, this user has been locked out." in error_message


def test_empty_credentials(page):
    """Test login with empty credentials on SauceDemo"""
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.login("", "")

    # Assert specific error message appears
    error_message = login_page.get_error_message()
    assert "Epic sadface: Username is required" in error_message
