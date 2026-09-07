
import csv
import time
from first_playwright_code.page_locators import practice_site_locators
from first_playwright_code.tests.test_practice_site import keyword

class CsvCreationPage:
    def __init__(self):
        self.keyword = keyword

    def mouse_over_web_table(self, xpath):
        try:
            self.keyword.mouse_over(xpath)
        except Exception as e:
            print(f"Error performing mouse over on web table: {e}")
            raise

    def get_row_count_for_web_table(self, xpath):
        try:
            return self.keyword.get_element_count(xpath)
        except Exception as e:
            print(f"Error getting row count for web table: {e}")
            raise
    
    def create_csv_file_for_web(self, file_path_pattern, xpath):
        try:
            timestamp = int(time.time())
            csv_path_web_table = self.keyword.create_a_csv_file(file_path_pattern.format(timestamp=timestamp))
            column_headers = [self.keyword.custom_get_text_if_fully_loaded(xpath.format(i=1, j=j)) for j in range(1, 4)]        
            self.keyword.create_a_csv_file(csv_path_web_table, column_headers)
            return csv_path_web_table
        except Exception as e:
            print(f"Error creating CSV file for web table: {e}")
            raise

    def write_data_to_csv_for_web(self, csv_path, row_count, xpath_for_column_names, xpath_for_cells):
        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                for i in range(1, row_count + 1):
                    row_data = []
                    for j in range(1, 4):  # Assuming there are 3 columns
                        if i == 1:
                            # Skip the header row as it is already written
                            extraction_xpath = xpath_for_column_names.format(i=i, j=j)
                        else:
                            extraction_xpath = xpath_for_cells.format(i=i, j=j)
                        cell_text = self.keyword.custom_get_text_if_fully_loaded(extraction_xpath)
                        row_data.append(cell_text)
                    csv_writer.writerow(row_data)
            self.keyword.verify_file_downloaded(csv_path)
        except Exception as e:
            print(f"Error writing data to CSV file for web table: {e}")
            raise