# First Playwright Code

This project is a small Playwright automation starter structured around reusable keyword libraries and page locators.

Project structure

- `keywords/common/`: shared browser utilities and reusable page-level actions
- `keywords/features/`: feature-specific workflow keywords
- `keywords/pages/`: page-level keyword wrappers
- `page_locators/`: locator constants for the target application
- `settings/`: framework configuration values
- `test_data/`: input data and static fixtures
- `tests/`: end-to-end test scripts
- `utils/`: helper functions used across the suite
- `logs/`: runtime logs generated during test execution

Core usage

The `Common` keyword class is exported from `first_playwright_code.keywords.common` and provides browser setup, navigation, element interaction, assertions, waits, and screenshots.

```python
from playwright.sync_api import sync_playwright
from first_playwright_code.keywords.common import Common

with sync_playwright() as playwright:
    keyword = Common(playwright)
    keyword.open_browser("chrome", "https://example.com")
    keyword.verify_visible("xpath=//button")
    keyword.close_browser()
```

Configuration

Timing values such as timeout and retry sleep intervals are defined in `settings/setting.yaml` and exposed through the common package:

```python
from first_playwright_code.keywords.common import DEFAULT_TIMEOUT, TIME_SLEEP

print(DEFAULT_TIMEOUT)
print(TIME_SLEEP["S"])
```

Setup and execution

Install dependencies and browser binaries before running the tests:

```bash
cd first_playwright_code
python3 -m pip install -r requirements.txt
python3 -m playwright install
python3 -m pytest tests
```

If you are running the project from a parent directory instead, use:

```bash
python3 -m pip install -r first_playwright_code/requirements.txt
python3 -m playwright install
python3 -m pytest first_playwright_code/tests
```

The repository currently includes a sample flow in `tests/test_practice_site.py` that opens a practice site, extracts web table data, writes it to CSV, and verifies the file was created.
