# qa-py-browserstack

Web, API and mobile tests in one pytest project, run on BrowserStack real browsers and devices, with optional TestRail and Jira reporting. Proof of concept.

| Suite | Tool | Target | Runs on |
|---|---|---|---|
| `tests/web` | Playwright | [SauceDemo](https://www.saucedemo.com) | Local Chromium or BrowserStack Automate |
| `tests/api` | Requests | [JSONPlaceholder](https://jsonplaceholder.typicode.com) | Locally |
| `tests/mobile` | Appium | [WebdriverIO native demo app](https://github.com/webdriverio/native-demo-app) | Local emulator or BrowserStack App Automate |

This repo combines the former `qa-py-playwright-browserstack` and `qa-py-appium-browserstack`, with both histories kept.

## Structure

```text
├── browserstack/
│   ├── web.yml            # Browsers for the web suite
│   └── mobile.yml         # Devices and app for the mobile suite
├── config/
│   └── mobile_capabilities.py   # Local Appium capabilities
├── pages/
│   ├── web/               # Playwright page objects
│   └── mobile/            # Appium page objects (Android and iOS locators)
├── tests/
│   ├── conftest.py        # Command-line options and the Jira failure hook
│   ├── api/
│   ├── mobile/            # conftest.py builds the Appium driver
│   └── web/
└── utils/
    ├── api_client.py
    └── jira_client.py
```

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run playwright install chromium
```

## Run locally

```bash
uv run pytest tests/api
uv run pytest tests/web            # add --headed to watch the browser
```

The mobile suite needs an Appium server on `http://127.0.0.1:4723` and an emulator or simulator. Download the demo app from the [v2.0.0 release](https://github.com/webdriverio/native-demo-app/releases/tag/v2.0.0) into `apps/android/` or `apps/ios/`, then:

```bash
uv run pytest tests/mobile --platform android
uv run pytest tests/mobile --platform ios
uv run pytest tests/mobile --platform android --app-path apps/custom.apk --device-name emulator-5554
```

| Flag | Values | Default |
|---|---|---|
| `--platform` | `android`, `ios` | `android` |
| `--app-path` | Path to an `.apk` or `.ipa` | from `config/mobile_capabilities.py` |
| `--device-name` | Emulator or simulator name | from `config/mobile_capabilities.py` |

`pytest.ini` turns the BrowserStack SDK plugin off for local runs, because it takes over driver setup. `browserstack-sdk pytest` turns it back on.

## Run on BrowserStack

The SDK reads `browserstack.yml` from the project root. Copy the config for the suite you want, then run through the SDK:

```bash
export BROWSERSTACK_USERNAME=...
export BROWSERSTACK_ACCESS_KEY=...

cp browserstack/web.yml browserstack.yml
uv run browserstack-sdk pytest tests/web

cp browserstack/mobile.yml browserstack.yml
uv sync --no-group web
uv run --no-sync browserstack-sdk pytest tests/mobile --platform android
uv sync                 # restore the full environment afterwards
```

The SDK decides which framework to hook into from the installed packages, and skips Appium when Playwright is installed. That's why the mobile cloud run needs an environment without the `web` group, and why `--no-sync` stops `uv run` from reinstalling it.

The root `browserstack.yml` is git-ignored. For mobile, the SDK uploads the app from `apps/android/` on each run, because BrowserStack deletes uploaded apps after 30 days.

## Reporting

Both integrations are off unless you pass their flag.

**TestRail** (`--testrail`): copy `testrail.cfg.example` to `testrail.cfg` and fill it in. Tests are linked with `@pytestrail.case("<id>")`.

**Jira** (`--jira`): copy `.env.example` to `.env` and fill it in. A failing test opens a bug, or comments on the open bug for that test instead of creating a duplicate. If Jira is unreachable, the run continues without it.

## CI

`.github/workflows/tests.yml` runs on every push and pull request:

1. **local**: lint, check that every suite collects, and run the API and web tests in local Chromium. Needs no secrets.
2. **browserstack**: runs the web and mobile suites on BrowserStack. Skipped with a notice when the secrets are missing.

| Setting | Type | Purpose |
|---|---|---|
| `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY` | Secret | Cloud runs |
| `ENABLE_TESTRAIL` = `true` | Variable | Report to TestRail, using the `TESTRAIL_URL`, `TESTRAIL_EMAIL` and `TESTRAIL_API_KEY` secrets |
| `ENABLE_JIRA` = `true` | Variable | File Jira bugs, using the `JIRA_URL`, `JIRA_EMAIL` and `JIRA_API_TOKEN` secrets, and optional `JIRA_PROJECT_KEY` and `JIRA_BOARD_ID` variables |
