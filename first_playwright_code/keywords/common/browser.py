from playwright.sync_api import Browser, Page, Playwright


def create_page(playwright: Playwright, base_url: str) -> tuple[Browser, Page]:
    """Create a Chromium page configured for the target application."""
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(base_url)
    return browser, page
