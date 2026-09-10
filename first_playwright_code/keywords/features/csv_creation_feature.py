from first_playwright_code.keywords.pages.csv_creation_page import CsvCreationPage
from first_playwright_code.keywords.common import Common
from first_playwright_code.page_locators import practice_site_locators

class CsvCreationFeature:
    def __init__(self, keyword: Common):
        self.csv_creation_page = CsvCreationPage(keyword)

    def create_csv_file_for_web_table(self):
        try:
            self.csv_creation_page.mouse_over_web_table(practice_site_locators.WEB_TABLE_XPATH)
            row_count_web_table = self.csv_creation_page.get_row_count_for_web_table(practice_site_locators.WEB_TABLE_ROW_XPATH)
            csv_path_web_table = self.csv_creation_page.create_csv_file_for_web(practice_site_locators.WEB_TABLE_DATA_CSV_PATH, practice_site_locators.WEB_TABLE_COLUMN_NAMES_XPATH)
            self.csv_creation_page.write_data_to_csv_for_web(
                csv_path_web_table,
                row_count_web_table,
                practice_site_locators.WEB_TABLE_COLUMN_NAMES_XPATH,
                practice_site_locators.WEB_TABLE_CELL_XPATH
            )
        except Exception as e:
            print(f"Error creating CSV files: {e}")
            raise

    def create_csv_file_for_web_fixed_table(self):
        try:
            row_count_web_fixed_table = self.csv_creation_page.get_row_count_for_web_table(practice_site_locators.WEB_TABLE_FIXED_HEADER_XPATH)
            csv_path_web_fixed_table = self.csv_creation_page.create_csv_file_for_web(practice_site_locators.WEB_TABLE_FIXED_HEADER_DATA_CSV_PATH, practice_site_locators.WEB_TABLE_FIXED_HEADER_COLUMN_NAMES_XPATH)
            self.csv_creation_page.write_data_to_csv_for_web(
                csv_path_web_fixed_table,
                row_count_web_fixed_table,
                practice_site_locators.WEB_TABLE_FIXED_HEADER_COLUMN_NAMES_XPATH,
                practice_site_locators.WEB_TABLE_FIXED_HEADER_CELL_XPATH
            )
        except Exception as e:
            print(f"Error creating CSV file for web fixed table: {e}")
            raise