import csv
import os
from pathlib import Path
import sys
import time
from typing import Any
import logging

from first_playwright_code.page_locators import practice_site_locators

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

from playwright.sync_api import Browser, Page, Playwright, expect

from .settings import DEFAULT_TIMEOUT, TIME_SLEEP, DEFAULT_UNWANTED_SYMBOLS


    

class Common:
    """Reusable Playwright keywords for page-level test actions."""

    def __init__(self, playwright: Playwright):
        """Initialize the common keyword library with a Playwright instance."""
        self.playwright = playwright
        self.browser: Browser | None = None
        self.page: Page | None = None

    def _require_page(self) -> Page:
        """Return the active page or report that the browser is not open."""
        if self.page is None:
            raise RuntimeError("The browser is not open. Call open_browser first.")
        return self.page

    def maximize_window(self) -> Page:
            """Maximize the browser window."""
            page = self._require_page()
            page.set_viewport_size({"width": page.evaluate("() => screen.width"), "height": page.evaluate("() => screen.height")})
            return page
    
    def open_browser(self, browser_name, url: str, headless: bool = False) -> Page:
        """Launch the specified browser, open a new page, and navigate to the given URL."""
        self.browser = self.playwright.chromium.launch(
            channel=browser_name,
            headless=headless,
            args=[
                "--start-maximized",
                "--disable-infobars",
                "--disable-extensions",
                "--disable-gpu",
                "--no-sandbox",
                "--kiosk-printing",
                "--disable-notifications",
                "--disable-popup-blocking",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                ""
            ],
        )
        self.page = self.browser.new_page()
        self.page.goto(url)
        self.page = self.maximize_window()
        logger.info("Browser opened")
        return self.page

    def check(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Check a visible checkbox or radio control."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).check(timeout=timeout)
        logger.info("Checked element: %s", xpath)

    def check_enabled(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        try:
            expect(
                self._require_page().locator(xpath)
            ).to_be_enabled(timeout=timeout)

            return True

        except AssertionError:
            return False

    def check_visible(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        try:
            expect(
                self._require_page().locator(xpath)
            ).to_be_visible(timeout=timeout)

            return True

        except AssertionError:
            return False

    def clear_element_text(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Clear the text of a visible input element."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).fill("", timeout=timeout)
        logger.info("Cleared text for element: %s", xpath)

    def clear_text(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Clear the text from an input element."""
        self.input_text(xpath, "", timeout)
        logger.info("Cleared text for element: %s", xpath)

    def click_element(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Click an enabled and visible element."""
        self.verify_visible(xpath, timeout)
        self.verify_enabled(xpath, timeout)
        self._require_page().locator(xpath).click(timeout=timeout)
        logger.info("Clicked: %s", xpath)

    def click_element_if_visible_and_enabled(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Click the element if it is visible and enabled."""
        page = self._require_page()
        locator = page.locator(xpath)
        if self.verify_visible(xpath, TIME_SLEEP["XL"]) and self.verify_enabled(xpath, TIME_SLEEP["XL"]):
            self.mouse_over(xpath)
            self.click(xpath, timeout)
            logger.info("Clicked element if it was visible and enabled: %s", xpath)
        else:
            raise TimeoutError("The element was not visible and enabled.")

    def click_element_javascript(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Click an element by executing its JavaScript click handler."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).evaluate("(element) => element.click()")
        logger.info("Clicked using JavaScript: %s", xpath)

    def close_browser(self) -> None:
        """Close the browser and clear the active browser and page references."""
        if self.browser is not None:
            self.browser.close()
            self.browser = None
            self.page = None
            logger.info("Closed the browser and cleared references.")

    def construct_csv_path(self, file_type, timestamp: int) -> str:
        """Format the CSV path for web table data using the given timestamp."""
        logger.info("Constructed CSV path: %s", file_type.format(timestamp))
        return file_type.format(timestamp)

    def create_a_csv_file(self, csv_path: str, column_headers) -> str:
        """Create a new CSV file for the specified path."""
        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(column_headers)
        logger.info("Created CSV file at path: %s with headers: %s", csv_path, column_headers)
        return csv_path    

    def custom_click_element_if_fully_loaded(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Click an element only if it is fully loaded and visible."""
        page = self._require_page()
        for attempt in range(5):
            if page.evaluate("document.readyState === 'complete'"):
                logger.info("Page fully loaded after %d attempts.", attempt + 1)
                break
            if attempt < 4:
                time.sleep(TIME_SLEEP["XL"])
        else:
            raise TimeoutError("The page was not fully loaded after 5 checks.")

        locator = page.locator(xpath)
        for attempt in range(5):
            enable_status = self.check_enabled(xpath, timeout=TIME_SLEEP["XL"] * 1000)
            visible_status = self.check_visible(xpath, timeout=TIME_SLEEP["XL"] * 1000)
            if visible_status == True  and enable_status == True:
                self.mouse_over(xpath)
                self.click_element(xpath, timeout)
                logger.info("Clicked element after ensuring it was fully loaded: %s", xpath)
                return
            if attempt < 4:
                logger.info(
                    "Element '%s' is not visible and enabled (visible: %s, enabled: %s), retrying... (attempt %d)",
                    xpath,
                    visible_status,
                    enable_status,
                    attempt + 1,
                )
                time.sleep(TIME_SLEEP["XL"])
            logger.info(
                "Element '%s' is not visible and enabled after %d seconds (visible: %s, enabled: %s), retrying... (attempt %d)",
                xpath,
                TIME_SLEEP["XL"],
                visible_status,
                enable_status,
                attempt + 1,
            )
        logger.error("The element '%s' was not visible and enabled after 5 checks and %d seconds.", xpath, TIME_SLEEP["XL"]*5)
        raise TimeoutError(f"The element '{xpath}' was not visible and enabled after 5 checks.")

    def custom_get_text_if_fully_loaded(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Get the text of an element only if it is fully loaded and visible."""
        page = self._require_page()
        for attempt in range(5):
            if page.evaluate("document.readyState === 'complete'"):
                logger.info("Page fully loaded after %d attempts.", attempt + 1)
                break
            if attempt < 4:
                time.sleep(TIME_SLEEP["XL"])
        else:
            raise TimeoutError("The page was not fully loaded after 5 checks.")

        locator = page.locator(xpath)
        for attempt in range(5):
            enable_status = self.check_enabled(xpath, timeout=TIME_SLEEP["XL"] * 1000)
            visible_status = self.check_visible(xpath, timeout=TIME_SLEEP["XL"] * 1000)
            if (visible_status and enable_status):
                self.mouse_over(xpath)
                text = self.get_text(xpath, timeout)
                logger.info("Got text from element after ensuring it was fully loaded: %s -> %s", xpath, text)
                return text
            if attempt < 4:
                time.sleep(TIME_SLEEP["XL"])
            logger.info(
                "Element '%s' is not visible and enabled after %d seconds (visible: %s, enabled: %s), retrying... (attempt %d)",
                xpath,
                TIME_SLEEP["XL"],
                visible_status,
                enable_status,
                attempt + 1,
            )
        logger.error("The element '%s' was not visible and enabled after 5 checks and %d seconds.", xpath, TIME_SLEEP["XL"]*5)
        raise TimeoutError(f"The element '{xpath}' was not visible and enabled after 5 checks and {TIME_SLEEP['XL']*5} seconds.")

    def custom_input_text_if_fully_loaded(self, xpath: str, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
            """Input text into an element only if it is fully loaded and visible."""
            page = self._require_page()
            for attempt in range(5):
                if page.evaluate("document.readyState === 'complete'"):
                    logger.info("Page fully loaded after %d attempts.", attempt + 1)
                    break
                if attempt < 4:
                    time.sleep(TIME_SLEEP["L"])
            else:
                raise TimeoutError("The page was not fully loaded after 5 checks.")
    
            locator = page.locator(xpath)
            for attempt in range(5):
                enable_status = self.check_enabled(xpath, timeout=TIME_SLEEP["XL"] * 1000)
                visible_status = self.check_visible(xpath, timeout=TIME_SLEEP["XL"] * 1000)
                if enable_status and visible_status:
                    self.mouse_over(xpath)
                    self.input_text(xpath, text, timeout)
                    logger.info("Input text into element after ensuring it was fully loaded: %s", xpath)
                    return
                if attempt < 4:
                    logger.info(
                        "Element '%s' is not visible and enabled (visible: %s, enabled: %s), retrying... (attempt %d)",
                        xpath,
                        visible_status,
                        enable_status,
                        attempt + 1,
                    )
                    time.sleep(TIME_SLEEP["S"])
                logger.info(
                    "Element '%s' is not visible and enabled after %d seconds (visible: %s, enabled: %s), retrying... (attempt %d)",
                    xpath,
                    TIME_SLEEP["XL"],
                    visible_status,
                    enable_status,
                    attempt + 1,
                )
            logger.error("The element '%s' was not visible and enabled after 5 checks and %d seconds.", xpath, TIME_SLEEP["XL"]*5)
            raise TimeoutError(f"The element '{xpath}' was not visible and enabled after 5 checks and {TIME_SLEEP['XL']*5} seconds.")

    def double_click_element(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Double-click an enabled and visible element."""
        self.verify_visible(xpath, timeout)
        self.verify_enabled(xpath, timeout)
        self._require_page().locator(xpath).dblclick(timeout=timeout)
        logger.info("Double-clicked: %s", xpath)

    def download_file_and_verify(self, xpath: str, download_path: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Download a file from the element identified by the given xpath."""
        page = self._require_page()
        self.verify_visible(xpath, timeout)
        self.verify_enabled(xpath, timeout)
        locator = page.locator(xpath)
        if self.verify_visible(xpath, TIME_SLEEP["XL"]) and self.verify_enabled(xpath, TIME_SLEEP["XL"]):
            with page.expect_download() as download_info:
                self.click(xpath, timeout)
            download = download_info.value
            download.save_as(download_path)
            logger.info("Downloaded file from element: %s -> %s", xpath, download_path)
            file_exists = os.path.exists(download_path)
            if not file_exists:
                raise TimeoutError("The downloaded file was not found at the specified path.")
        else:
            raise TimeoutError("The element was not visible and enabled for file download.")

    def evaluate(self, expression: str, arg: Any = None) -> Any:
        """Evaluate JavaScript in the active page."""
        evaluated = self._require_page().evaluate(expression, arg)
        logger.info("Evaluated expression: %s -> %s", expression, evaluated)
        return evaluated

    def get_attribute(self, xpath: str, attribute: str, timeout: int = DEFAULT_TIMEOUT) -> str | None:
        """Return an attribute value from a visible element."""
        self.verify_visible(xpath, timeout)
        value = self._require_page().locator(xpath).get_attribute(
            attribute,
            timeout=timeout,
        )
        logger.info("Got attribute '%s' for element: %s -> %s", attribute, xpath, value)
        return value

    def get_element_count(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> int:
        """Get the count of elements matching the xpath"""
        #page = self._require_page()
        page = self._require_page()
        locator = page.locator(xpath)
        count = locator.count()  # Use the locator defined above
        logger.info("Got element count for xpath: %s -> %d", xpath, count)
        return count

    def get_text(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Return the inner text of a visible element."""
        self.verify_visible(xpath, timeout)
        self.mouse_over(xpath, timeout)
        text = self._require_page().locator(xpath).inner_text(timeout=timeout)
        logger.info("Got text for element: %s -> %s", xpath, text)
        return text

    def get_text_javascript(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Return an element's inner text by executing JavaScript."""
        self.verify_visible(xpath, timeout)
        text = self._require_page().locator(xpath).evaluate("(element) => element.innerText")
        logger.info("Got text via JavaScript for element: %s -> %s", xpath, text)
        return text

    def get_value(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Return the current value of a visible input element."""
        self.verify_visible(xpath, timeout)
        value = self._require_page().locator(xpath).input_value(timeout=timeout)
        logger.info("Got value for element: %s -> %s", xpath, value)
        return value

    def goto(self, url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Navigate the active page to a URL."""
        self._require_page().goto(url, timeout=timeout)

    def input_text(self, xpath: str, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Fill an enabled and visible input with text."""
        self.verify_visible(xpath, timeout)
        self.verify_enabled(xpath, timeout)
        self._require_page().locator(xpath).fill(text, timeout=timeout)
        logger.info("Entered text: %s", xpath)

    def keyboard_type(self, xpath: str, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Wait for an element, focus it, and type text using the keyboard."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).focus(timeout=timeout)
        self._require_page().keyboard.type(text)
        logger.info("Typed text using keyboard for element: %s", xpath)

    def mouse_over(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Move the mouse pointer over a visible element."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).hover(timeout=timeout)
        logger.info("Mouse over on element: %s", xpath)

    def press_key(self, xpath: str, key: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Press a keyboard key on a visible element."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).press(key, timeout=timeout)
        logger.info("Pressed key '%s' for element: %s", key, xpath)

    def refresh(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Reload the active page."""
        self._require_page().reload(timeout=timeout)
        logger.info("Page refreshed")

    def remove_unwanted_symbol_from_text(self, text: str, unwanted_symbols: str = DEFAULT_UNWANTED_SYMBOLS) -> str:
        """Remove unwanted symbols from text, using the default symbol set when omitted."""
        cleaned_text = text.translate(str.maketrans("", "", unwanted_symbols))
        logger.info("Removed unwanted symbols from text: %s -> %s", text, cleaned_text)
        return cleaned_text

    def scroll_to_element(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Scroll a visible element into the viewport."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).scroll_into_view_if_needed(
            timeout=timeout
        )
        logger.info("Scrolled to element: %s", xpath)

    def select_frame(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Select the frame identified by the given xpath."""
        page = self._require_page()
        self.verify_visible(xpath)
        self.verify_enabled(xpath)
        locator = page.locator(xpath)
        frame_element = locator.element_handle()
        if frame_element is None:
            raise TimeoutError("The frame element was not found.")
        page.frame_locator(f"xpath={xpath}").frame(element=frame_element)
        logger.info("Selected frame for xpath: %s", xpath)

    def select_option(self, xpath: str, value: str | list[str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """Select one or more values from a dropdown element."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).select_option(value, timeout=timeout)
        logger.info("Selected option '%s' for element: %s", value, xpath)

    def switch_to_second_window(self) -> Page:
        """Switch to a second window after up to five one-second checks."""
        page = self._require_page()
        for attempt in range(5):
            pages = page.context.pages
            if len(pages) >= 2:
                self.page = pages[1]
                return self.page
            if attempt < 4:
                time.sleep(TIME_SLEEP["S"])
                logger.info("Second window not found, attempt %d", attempt + 1)
        logger.error("Failed to find a second window after 5 attempts.")
        raise TimeoutError("A second browser window was not available after 5 checks in 5 seconds.")
        

    def take_screenshot(self, path: str, full_page: bool = True) -> None:
        """Save a screenshot of the active page."""
        screenshot_path = Path(path)
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        self._require_page().screenshot(path=str(screenshot_path), full_page=full_page)
        logger.info("Saved screenshot to: %s", screenshot_path)

    def uncheck(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Uncheck a visible checkbox."""
        self.verify_visible(xpath, timeout)
        self._require_page().locator(xpath).uncheck(timeout=timeout)
        logger.info("Unchecked element: %s", xpath)

    def upload_file(self, xpath: str, file_path: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Upload a file to the element identified by the given xpath."""
        page = self._require_page()
        self.verify_visible(xpath, timeout)
        self.verify_enabled(xpath, timeout)
        locator = page.locator(xpath)
        if self.verify_visible(xpath, TIME_SLEEP["XL"]) and self.verify_enabled(xpath, TIME_SLEEP["XL"]):
            locator.set_input_files(file_path)
            logger.info("Uploaded file to element: %s -> %s", xpath, file_path)
        else:
            raise TimeoutError("The element was not visible and enabled for file upload.")

    def verify_checked(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Verify that a checkbox or radio control is checked."""
        self.verify_visible(xpath, timeout)
        expect(self._require_page().locator(xpath)).to_be_checked(timeout=timeout)
        logger.info("Verified element is checked: %s", xpath)

    def verify_disabled(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Verify that an element is disabled."""
        try:
            expect(self._require_page().locator(xpath)).to_be_disabled(timeout=timeout)
            logger.info("Element disabled: %s", xpath)
        except AssertionError:
            logger.error("Element not disabled: %s", xpath)
            raise

    def verify_enabled(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Verify that an element is enabled."""
        try:
            expect(self._require_page().locator(xpath)).to_be_enabled(timeout=timeout)
            logger.info("Element enabled: %s", xpath)
        except AssertionError:
            logger.error("Element not enabled: %s", xpath)
            raise

    def verify_file_downloaded(self, download_path: str) -> None:
        """Verify that the file exists at the specified download path."""
        file_exists = os.path.exists(download_path)
        if not file_exists:
            raise TimeoutError("The downloaded file was not found at the specified path.")
        logger.info("Verified file exists at download path: %s", download_path)

    def verify_hidden(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Verify that an element is hidden."""
        try:
            expect(self._require_page().locator(xpath)).to_be_hidden(timeout=timeout)
            logger.info("Element hidden: %s", xpath)
        except AssertionError:
            logger.error("Element not hidden: %s", xpath)
            raise

    def verify_text(self, xpath: str, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Verify that an element contains the expected text."""
        expect(self._require_page().locator(xpath)).to_contain_text(
            text,
            timeout=timeout,
        )
        logger.info("Verified text for element: %s", xpath)

    def verify_visible(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Verify that an element is visible."""
        status = False
        try:
            expect(self._require_page().locator(xpath)).to_be_visible(timeout=timeout)
            logger.info("Element visible: %s", xpath)
            status = True
            return status
        except AssertionError:
            logger.error("Element not visible: %s", xpath)
            raise

    def wait_for_load_state(self, state: str = "load", timeout: int = DEFAULT_TIMEOUT) -> None:
        """Wait for the active page to reach a load state."""
        self._require_page().wait_for_load_state(state, timeout=timeout)
        logger.info("Waited for load state: %s", state)

    def wait_for_url(self, url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Wait until the active page reaches the expected URL."""
        self._require_page().wait_for_url(url, timeout=timeout)
        logger.info("Waited for URL: %s", url)

