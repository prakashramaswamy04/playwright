from collections.abc import Generator
from datetime import datetime
import logging
from pathlib import Path
import time
import os
import csv

from playwright.sync_api import Browser, Page, sync_playwright

from first_playwright_code.keywords.common import Common
from first_playwright_code.page_locators import practice_site_locators

def configure_run_logging() -> tuple[logging.Logger, logging.FileHandler]:
    """Create a new timestamped log file for the current run."""
    logs_folder = Path(__file__).resolve().parents[1] / "logs"
    logs_folder.mkdir(parents=True, exist_ok=True)
    log_file = logs_folder / f"run_{datetime.now():%Y%m%d_%H%M%S_%f}.log"
    root_logger = logging.getLogger()
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root_logger.addHandler(file_handler)
    return root_logger, file_handler


def main() -> None:
    root_logger, file_handler = configure_run_logging()
    with sync_playwright() as playwright:
        keyword = Common(playwright)
        try:
            root_logger.info("Test run started")
            keyword.open_browser("chrome", practice_site_locators.PRACTICE_SITE_URL)
            # time.sleep(5)
            # for i in range(1, 4):
            #     keyword.check(getattr(practice_site_locators, f"RADIO_BUTTON_XPATH_{i}"))
            #     time.sleep(1)
            # keyword.custom_input_text_if_fully_loaded(practice_site_locators.CLASS_EXAMPLE_XPATH, "Sample Text")
            # for i in range(1, 4):
            #     keyword.select_option(getattr(practice_site_locators, "DROPDOWN_XPATH"), f"Option{i}")
            #     time.sleep(1)           
            # for i in range(1, 4):
            #     keyword.check(getattr(practice_site_locators, f"CHECKBOX_XPATH_{i}"))
            #     time.sleep(1)
            # #keyword.input_text(practice_site_locators.CLASS_EXAMPLE_XPATH, "Sample Text")
            # keyword.scroll_to_element(practice_site_locators.CLASS_EXAMPLE_XPATH)
            # keyword.mouse_over(practice_site_locators.MOUSE_HOVER_XPATH)
            # keyword.click_element(practice_site_locators.MOUSE_HOVER_TOP_XPATH)
            # time.sleep(1)
            # keyword.scroll_to_element(practice_site_locators.CLASS_EXAMPLE_XPATH)
            keyword.scroll_to_element(practice_site_locators.WEB_TABLE_XPATH)
            row_count = keyword.get_element_count(practice_site_locators.WEB_TABLE_ROW_XPATH)


            timestamp = int(time.time())
            csv_path = keyword.construct_csv_path(practice_site_locators.WEB_TABLE_DATA_CSV_PATH, timestamp)
            column_headers = [keyword.custom_get_text_if_fully_loaded(practice_site_locators.WEB_TABLE_COLUMN_NAME_XPATH.format(i=1, j=j)) for j in range(1, 4)]
            keyword.create_a_csv_file(csv_path, column_headers)
            with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                for i in range(1, row_count + 1):
                    row_data = []
                    for j in range(1, 4):  # Assuming there are 3 columns
                        if i == 1:
                            # Skip the header row as it is already written
                            extraction_xpath = practice_site_locators.WEB_TABLE_COLUMN_NAME_XPATH.format(i=i, j=j)
                        else:
                            extraction_xpath = practice_site_locators.WEB_TABLE_CELL_XPATH.format(i=i, j=j)                        
                        cell_text = keyword.custom_get_text_if_fully_loaded(extraction_xpath)
                        root_logger.info("Cell text at row %d, column %d: %s", i, j, cell_text)
                        row_data.append(cell_text)
                    csv_writer.writerow(row_data)
            keyword.verify_file_downloaded(csv_path)
            fixed_header_row_count = keyword.get_element_count(practice_site_locators.WEB_TABLE_FIXED_HEADER_XPATH)
            timestamp = int(time.time())
            fixed_header_csv_path = keyword.construct_csv_path(practice_site_locators.WEB_TABLE_FIXED_HEADER_DATA_CSV_PATH, timestamp)
            fixed_header_column_headers = [keyword.custom_get_text_if_fully_loaded(practice_site_locators.WEB_TABLE_FIXED_HEADER_COLUMN_NAME_XPATH.format(i=1, j=j)) for j in range(1, 4)]
            keyword.create_a_csv_file(fixed_header_csv_path, fixed_header_column_headers)
            with open(fixed_header_csv_path, "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                for i in range(1, fixed_header_row_count + 1):
                    row_data = []
                    for j in range(1, 4):  # Assuming there are 3 columns
                        if i == 1:
                            # Skip the header row as it is already written
                            extraction_xpath = practice_site_locators.WEB_TABLE_FIXED_HEADER_XPATH.format(i=i, j=j)
                        else:
                            extraction_xpath = practice_site_locators.WEB_TABLE_FIXED_HEADER_CELL_XPATH.format(i=i, j=j)
                        cell_text = keyword.custom_get_text_if_fully_loaded(extraction_xpath)
                        root_logger.info("Fixed header cell text at row %d, column %d: %s", i, j, cell_text)
                        row_data.append(cell_text)
                    csv_writer.writerow(row_data)
            keyword.verify_file_downloaded(fixed_header_csv_path)
            time.sleep(10)
        finally:
            keyword.close_browser()
            root_logger.info("Test run finished")
            root_logger.removeHandler(file_handler)
            file_handler.close()

if __name__ == "__main__":
    main()
