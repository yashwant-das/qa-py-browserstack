# Playwright + Pytest + BrowserStack POC Framework

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?logo=python&logoColor=white) ![Playwright](https://img.shields.io/badge/Playwright-Enabled-2EAD33?logo=playwright&logoColor=white) ![pytest](https://img.shields.io/badge/pytest-Testing-0A9EDC?logo=pytest&logoColor=white) ![uv](https://img.shields.io/badge/uv-Fast_Deps-DE5FE9) ![BrowserStack](https://img.shields.io/badge/BrowserStack-Cloud-FF6600?logo=browserstack&logoColor=white) ![TestRail](https://img.shields.io/badge/TestRail-Integration-1F67AA) ![Jira](https://img.shields.io/badge/Jira-Defects-0052CC?logo=jira&logoColor=white)

This is a Proof-of-Concept (POC) cross-browser test automation framework built with Python, Pytest, Playwright, and integrated with BrowserStack for cloud execution.

## Features

- **Page Object Model (POM):** Setup for web UI tests (`pages/base_page.py`, `pages/login_page.py`).
- **Playwright Setup:** Native `pytest-playwright` integration for UI interaction.
- **API Testing:** Utility to test APIs (`utils/api_client.py`). Tested using `jsonplaceholder.typicode.com`.
- **BrowserStack Integration:** Ready-to-use cross-browser scaling with `browserstack-sdk`.

## Project Structure

```text
├── browserstack.yml     # BrowserStack execution configuration
├── pages/
│   ├── base_page.py     # Base framework wrapper for elements 
│   └── login_page.py    # Example POM logic
├── pyproject.toml       # Dependencies configuration
├── tests/
│   ├── api/
│   │   └── test_api.py          # Examples of REST API testing
│   ├── web/
│   │   └── test_login_page.py   # Web specs matching page objects
│   └── conftest.py              # Pytest global fixtures
└── utils/
    └── api_client.py    # API Utility requests
```

## Setup & Run Local Tests

1.  **Install dependencies using UV:**

    ```bash
    uv sync
    ```
    *Make sure you have python 3.12+ installed.*

2.  **Install Playwright Browsers:**

    ```bash
    uv run playwright install chromium
    ```

3.  **Run Local Web Tests:**

    ```bash
    uv run pytest tests/web/
    ```

4.  **Run Local API Tests:**

    ```bash
    uv run pytest tests/api/
    ```

5.  **Useful Pytest Flags:**

    *   **UI Mode:** To see the browser while running web tests, pass the `--headed` flag: 
        `uv run pytest tests/web/test_login_page.py --headed`
    *   **HTML Report:** To generate an HTML test report, pass the `--html` flag: 
        `uv run pytest tests/web/ --html=test-results/report.html`

## Run Tests on BrowserStack

This framework integrates with the BrowserStack SDK for cloud execution. It targets multiple OS and Browser combination natively as specified in `browserstack.yml`.

1.  **Set Environment Variables:**
    Export your BrowserStack credentials.

    ```bash
    export BROWSERSTACK_USERNAME="YOUR_USERNAME"
    export BROWSERSTACK_ACCESS_KEY="YOUR_ACCESS_KEY"
    ```

2.  **Run the Tests using the SDK:**

    ```bash
    uv run browserstack-sdk pytest tests/web/
    ```

You can view the test results directly in the BrowserStack Automate dashboard.

## TestRail Integration

This repository is integrated with TestRail via the `pytest-testrail` plugin.

1. **Configure Credentials:** Copy the included `testrail.cfg.example` to a new file named `testrail.cfg` (which is git-ignored for safety) and fill in your details:
   ```ini
   [API]
   url = https://yourdomain.testrail.io/
   email = your_email@example.com
   password = your_api_key
   
   [TESTRUN]
   project_id = 1
   ```
2. **Tag Tests:** Decorate your Pytest definitions with their TestRail ID:
   ```python
   from pytest_testrail.plugin import pytestrail
   
   @pytestrail.case("1234")
   def test_successful_login(page):
   ```
3. **Execute & Push:** When you run tests with the testrail flag, the results automatically update in TestRail:
   ```bash
   uv run pytest tests/web/ --testrail
   # Or via BrowserStack
   uv run browserstack-sdk pytest tests/web/ --testrail
   ```

## Jira Integration

This repository automatically generates Jira Bug tickets whenever an automated test fails.

1. **Configure Credentials:** The architecture listens for your Jira credentials in a secure `.env` file at the root. Copy the included `.env.example` to a new file named `.env` (which is git-ignored) and populate it:
   ```env
   JIRA_URL=https://yourcompany.atlassian.net
   JIRA_EMAIL=your_email@example.com
   JIRA_API_TOKEN=your_jira_api_token
   JIRA_PROJECT_KEY=SCRUM
   JIRA_BOARD_ID=1
   ```
2. **Execution:** Pass the `--jira` flag when running tests:
   ```bash
   uv run pytest tests/web/ --jira
   # Or combine both
   uv run pytest tests/web/ --testrail --jira
   ```
   The Pytest `makereport` hook inside `tests/conftest.py` will intercept the run. If a test fails, it captures the `AssertionError` traceback and pushes it to Jira.
3. **Deduplication:** To avoid spamming your Jira board, the `JiraClient` searches for existing open bugs matching the failed Test Name. If an open bug already exists, it simply adds a comment with the latest failure traceback instead of creating a duplicate ticket!

## CI/CD Secret Management

To keep your credentials secure while executing successfully in your GitHub Actions pipeline, the `.github/workflows/playwright-tests.yml` natively consumes **GitHub Secrets** and constructs your config files automatically on the fly during the pipeline run. 

Add the following keys to your repository's: `Settings > Secrets and variables > Actions`:

* `BROWSERSTACK_USERNAME` 
* `BROWSERSTACK_ACCESS_KEY`
* `JIRA_URL` 
* `JIRA_EMAIL`
* `JIRA_API_TOKEN`
* `TESTRAIL_URL`  *(e.g., https://yourcompany.testrail.io/)*
* `TESTRAIL_EMAIL`
* `TESTRAIL_API_KEY`

Because the pipeline writes `testrail.cfg` dynamically and passes Jira credentials directly into standard Environment Variables (`env:`), your `.env` and `testrail.cfg` files will safely remain untracked locally without breaking your CI!
