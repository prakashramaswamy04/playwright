import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )

    page = browser.new_page()
    page.goto("https://www.google.com")
    time.sleep(5)  # Sleep for 5 seconds

    browser.close()