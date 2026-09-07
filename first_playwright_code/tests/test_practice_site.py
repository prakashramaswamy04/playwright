from collections.abc import Generator
import time
import csv
import pytest

from playwright.sync_api import sync_playwright

from first_playwright_code.keywords.common import Common
from first_playwright_code.page_locators import practice_site_locators
from first_playwright_code.utils.logging_utils import configure_run_logging
from first_playwright_code.keywords.features.basic_feature import BasicFeature
from first_playwright_code.keywords.features.csv_creation_feature import CsvCreationFeature

@pytest.fixture
def keyword() -> Generator[Common, None, None]:
    """Create and clean up the shared Playwright keyword object."""
    with sync_playwright() as playwright:
        keyword = Common(playwright)
        yield keyword
        keyword.close_browser()


def test_practice_site_workflow(keyword: Common) -> None:
    """Execute the practice-site automation workflow."""
    root_logger, file_handler = configure_run_logging()
    try:
        root_logger.info("Test run started")
        keyword.open_browser("chrome", practice_site_locators.PRACTICE_SITE_URL, headless=False)
        basic_action = BasicFeature()
        csv_creation_feature = CsvCreationFeature()
        basic_action.perform_basic_action()
        basic_action.perform_basic_mouse_over()
        csv_creation_feature.create_csv_file_for_web_table()
        csv_creation_feature.create_csv_file_for_web_fixed_table()
        time.sleep(10)
    finally:
        root_logger.info("Test run finished")
        file_handler.flush()
        root_logger.removeHandler(file_handler)
        file_handler.close()
