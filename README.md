# Appium + Pytest + BrowserStack POC Framework

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?logo=python&logoColor=white)  ![Appium](https://img.shields.io/badge/Appium-Mobile-66595C?logo=appium&logoColor=white)  ![pytest](https://img.shields.io/badge/pytest-Testing-0A9EDC?logo=pytest&logoColor=white)  ![uv](https://img.shields.io/badge/uv-Fast_Deps-DE5FE9) ![BrowserStack](https://img.shields.io/badge/BrowserStack-Cloud-FF6600?logo=browserstack&logoColor=white) ![TestRail](https://img.shields.io/badge/TestRail-Integration-1F67AA) ![Jira](https://img.shields.io/badge/Jira-Defects-0052CC?logo=jira&logoColor=white)

This is a Proof-of-Concept (POC) mobile App automation framework built with Python, Pytest, Appium, and integrated natively with BrowserStack for unified cross-device cloud execution.

- **Unified Page Object Model (POM):** Supports handling iOS and Android locators dynamically within the same Page Object class.
- **Pure Appium Setup:** Direct `appium-python-client` configuration abstracted inside modular Pytest fixtures.
- **BrowserStack Integration:** Unified cloud scaling with the `browserstack-sdk` and automatic app binary orchestration.
- **Local App Management:** Centralized `apps/` directory for `.ipa` and `.apk` storage with automatic local path resolution.

---

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

3.  **Local Execution Configuration:**
    The project uses a `pytest.ini` file to explicitly disable the BrowserStack SDK plugin during local runs (`addopts = -p no:browserstack_sdk`). 
    
    This is required because the `browserstack_sdk` auto-injects itself and intercepts Appium driver initialization. Disabling it ensures standard `appium:app` capabilities load seamlessly onto your local emulators without cloud interference.

4.  **Run Local Mobile Tests:**
    
    The Appium driver dynamically generates capabilities based on custom Pytest CLI arguments. Here are several ways to execute the tests:

    **Run on Android (Default):**
    ```bash
    uv run pytest tests/mobile/test_login.py --platform android
    ```

    **Run on iOS:**
    ```bash
    uv run pytest tests/mobile/test_login.py --platform ios
    ```

    **Run on a specific emulator with a custom APK path:**
    ```bash
    uv run pytest tests/mobile/test_login.py --platform android --app-path apps/custom.apk --device-name "emulator-5554"
    ```

    **Run with Jira defect creation enabled:**
    ```bash
    uv run pytest tests/mobile/test_login.py --platform ios --jira
    ```
    
### Available CLI Flags

The `driver` fixture recognizes the following flags to customize execution:

| Flag | Options | Description | Default |
| :--- | :--- | :--- | :--- |
| `--platform` | `android`, `ios` | Targets the specific mobile platform. | `android` |
| `--app-path` | Path string | Explicit path to an application binary. | `None` |
| `--device-name`| String | Precise name of the local emulator/simulator. | `None` |
| `--jira` | Boolean | Enable automatic Jira defect creation. | `False` |
| `--testrail` | Boolean | Enable TestRail result synchronization. | `False` |

## Run Tests on BrowserStack

This framework is natively integrated with the BrowserStack SDK for unified cloud execution across real Android and iOS devices.

> [!TIP]
> Executing tests via the `browserstack-sdk` CLI wrapper automatically overrides the local Appium configuration and handles automatic application uploads.

### 1. Set Credentials

Export your BrowserStack credentials as environment variables (recommended to add these to your `~/.zshrc` or `~/.bashrc`):

```bash
export BROWSERSTACK_USERNAME="YOUR_USERNAME"
export BROWSERSTACK_ACCESS_KEY="YOUR_ACCESS_KEY"
```

### 2. Configure Apps & Devices

The `browserstack.yml` file at the root manages your cloud configuration.

- **Auto-Upload:** Point the `app` key to your local `.apk` or `.ipa` path. The SDK will automatically upload and cache the app before execution.
- **Platforms:** Define the real devices and OS versions you want to target.

### 3. Execution Commands

The SDK wraps standard `pytest` commands. You can run tests individually, by directory, or combine them with reporting flags.

| Scope | Command |
| :--- | :--- |
| **Full Suite** | `uv run browserstack-sdk pytest tests/mobile/` |
| **Android Only** | `uv run browserstack-sdk pytest tests/mobile/ --platform android` |
| **iOS Only** | `uv run browserstack-sdk pytest tests/mobile/ --platform ios` |
| **Specific File** | `uv run browserstack-sdk pytest tests/mobile/test_login.py` |
| **With Jira** | `uv run browserstack-sdk pytest tests/mobile/ --jira` |
| **With TestRail** | `uv run browserstack-sdk pytest tests/mobile/ --testrail` |

> [!NOTE]
> Parallelism is managed via `parallelsPerPlatform` in `browserstack.yml`. The SDK handles session distribution automatically across your available BrowserStack parallel threads.

### 4. Viewing Results

After execution starts, the CLI will provide a direct link to the **BrowserStack App Automate** dashboard where you can view live video recordings, device vitals, and network logs.

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
