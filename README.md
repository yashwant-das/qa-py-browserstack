# Appium + Pytest + BrowserStack POC Framework

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?logo=python&logoColor=white)  ![Appium](https://img.shields.io/badge/Appium-Mobile-66595C?logo=appium&logoColor=white)  ![pytest](https://img.shields.io/badge/pytest-Testing-0A9EDC?logo=pytest&logoColor=white)  ![uv](https://img.shields.io/badge/uv-Fast_Deps-DE5FE9) ![BrowserStack](https://img.shields.io/badge/BrowserStack-Cloud-FF6600?logo=browserstack&logoColor=white) ![TestRail](https://img.shields.io/badge/TestRail-Integration-1F67AA) ![Jira](https://img.shields.io/badge/Jira-Defects-0052CC?logo=jira&logoColor=white)

This is a Proof-of-Concept (POC) mobile App automation framework built with Python, Pytest, Appium, and integrated natively with BrowserStack for unified cross-device cloud execution.

## Features

- **Unified Page Object Model (POM):** Supports handling iOS and Android locators dynamically within the same Page Object class (`pages/base_page.py`, `pages/login_page.py`).
- **Appium Setup:** Pure `appium-python-client` configuration abstracted inside Pytest fixtures.
- **BrowserStack Integration:** Ready-to-use cloud mobile scaling with `browserstack-sdk`.
- **Local App Builds:** Pre-configured `apps/` directory to store `.ipa` and `.apk` files.

## Project Structure

```text
├── apps/                # Store .apk or .ipa files here for app upload
├── browserstack.yml     # BrowserStack device & app execution config
├── pages/
│   ├── base_page.py     # Base framework wrapper for mobile elements (Explicit Waits)
│   └── login_page.py    # Example POM logic dynamically querying Android/iOS
├── pyproject.toml       # Dependencies configuration
├── tests/
│   ├── mobile/
│   │   └── test_login.py  # Mobile specs matching page objects
│   └── conftest.py      # Pytest global fixtures & Jira defect hook
└── utils/
    ├── jira_client.py   # Jira integration client
    └── api_client.py    # API Utility 
```

## Setup & Run Local Tests

1.  **Install dependencies using UV:**

    ```bash
    uv sync
    ```
    *Make sure you have python 3.12+ installed.*

2.  **Appium Server:**
    Ensure you have an Appium Server running locally (`http://127.0.0.1:4723`) and a local emulator/simulator setup if you wish to run completely bare-metal.

3.  **Run Local Mobile Tests:**
    
    The Appium driver dynamically generates capabilities based on custom Pytest CLI arguments.

    ```bash
    uv run pytest tests/mobile/ --platform=android --app-path=apps/sample.apk --device-name="emulator-5554"
    ```
    
    **Available CLI Flags:**
    * `--platform`: Options are `android` or `ios` (Default: `android`)
    * `--app-path`: Absolute or relative path to your compiled application binary. (Default: None)
    * `--device-name`: The precise name of the emulator/simulator. (Default: None)

## Run Tests on BrowserStack

This framework interacts directly with the BrowserStack SDK for unified cloud execution across disparate operating systems defined in `browserstack.yml`.

1.  **Set Environment Variables:**
    Export your BrowserStack credentials.

    ```bash
    export BROWSERSTACK_USERNAME="YOUR_USERNAME"
    export BROWSERSTACK_ACCESS_KEY="YOUR_ACCESS_KEY"
    ```

2.  **Define the App Url:**
    Upload your `.apk` or `.ipa` to Browserstack (via curl/API or BrowserStack UI) and update the `app: bs://<hash>` keys inside `browserstack.yml`.

3.  **Run the Tests via the SDK:**

    ```bash
    uv run browserstack-sdk pytest tests/mobile/
    ```

You can view the mobile test recordings directly in the BrowserStack App Automate dashboard.

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
   def test_successful_login(driver):
   ```
3. **Execute:** Pass the `--testrail` flag.
   ```bash
   uv run browserstack-sdk pytest tests/mobile/ --testrail
   ```

## Jira Integration

This repository automatically generates Jira Bug tickets whenever an automated test fails.

1. **Configure Credentials:** Copy `.env.example` to `.env` (git-ignored) and populate it:
   ```env
   JIRA_URL=https://yourcompany.atlassian.net
   JIRA_EMAIL=your_email@example.com
   JIRA_API_TOKEN=your_jira_api_token
   JIRA_PROJECT_KEY=SCRUM
   JIRA_BOARD_ID=1
   ```
2. **Execution:** Pass the `--jira` flag when running tests:
   ```bash
   uv run pytest tests/mobile/ --jira
   ```
   The `makereport` hook inside `tests/conftest.py` intercepts the run. If a test fails, it captures the Appium stack traceback and pushes it to Jira.
3. **Deduplication:** The `JiraClient` prevents spam by commenting on open identical issues rather than creating duplicates.

## CI/CD Secret Management

The `.github/workflows/appium-tests.yml` natively consumes **GitHub Secrets** and constructs config files dynamically on the fly. 

Add the following keys to your repository's: `Settings > Secrets and variables > Actions`:

* `BROWSERSTACK_USERNAME` 
* `BROWSERSTACK_ACCESS_KEY`
* `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
* `TESTRAIL_URL`, `TESTRAIL_EMAIL`, `TESTRAIL_API_KEY`
