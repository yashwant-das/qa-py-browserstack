from pages.login_page import LoginPage
from pytest_testrail.plugin import pytestrail


class TestWikipediaSearch:
    @pytestrail.case("C12345")
    def test_search_wikipedia_successfully(self, driver):
        """
        Test that searching for a term yields results.
        Runs dynamically on whatever platform BrowserStack routes to.
        """
        page = LoginPage(driver)

        search_term = "BrowserStack"
        page.perform_search(search_term)

        results = page.get_search_results()

        assert len(results) > 0, "No search results returned!"

        # Verify that at least one result contains our search term (case-insensitive)
        found_match = any(search_term.lower() in result.lower() for result in results)
        assert found_match is True, (
            f"Search term '{search_term}' not found in any result: {results}"
        )

    @pytestrail.case("C12346")
    def test_search_results_failure_example(self, driver):
        """
        This test is intentionally designed to fail to demonstrate
        the Jira and TestRail defect integration.
        """
        page = LoginPage(driver)

        page.perform_search("NonsenseTermThatShouldNotReturnResults1234")

        results = page.get_search_results()

        # This assertion will fail because the list *should* be empty
        assert len(results) > 50, "Intentional failure to trigger Jira Hook!"
