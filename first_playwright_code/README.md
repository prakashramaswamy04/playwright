# First Playwright Code

Python Playwright automation starter organized with the Page Object Model:

- `keywords/common/`: shared browser and test configuration
- `keywords/features/`: feature-level workflows
- `keywords/pages/`: reusable page actions
- `page_locators/`: page-specific selectors
- `test_data/`: test inputs and static fixtures
- `tests/`: automated test cases
- `utils/`: generic helpers

Reusable Playwright keywords are available through
`first_playwright_code.keywords.common.Common`, including browser lifecycle, navigation,
element interaction, assertions, waits, and screenshots.

Project timing values are stored in `settings/setting.yaml`:

```python
from first_playwright_code.keywords.common import DEFAULT_TIMEOUT, TIME_SLEEP

time.sleep(TIME_SLEEP["S"])
```

Install Playwright and its browser binaries before running the tests:

```bash
pip install -r first_playwright_code/requirements.txt
playwright install
pytest first_playwright_code/tests
```
