# Playwright + Pytest + BrowserStack POC Framework

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
│   ├── conftest.py      # Pytest global fixtures
│   ├── test_api.py      # Examples of REST API testing
│   └── test_web.py      # Examples of Web UI testing
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

3.  **Run All Tests Locally:**

    ```bash
    uv run pytest tests/
    ```

    *   To see the browser UI while running, pass the `--headed` flag: `uv run pytest tests/test_web.py --headed`
    *   To generate an HTML report in the standard Playwright directory, pass the `--html` flag: `uv run pytest tests/ --html=test-results/report.html --self-contained-html`

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
    uv run browserstack-sdk pytest tests/
    ```

You can view the test results directly in the BrowserStack Automate dashboard.
