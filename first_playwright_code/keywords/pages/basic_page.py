
import time
from first_playwright_code.keywords.common import Common
from first_playwright_code.page_locators import practice_site_locators

class BasicPage:

    def __init__(self, keyword: Common):
        self.keyword = keyword

    def select_radio_button(self):
        try:
            # Code to select the radio button using the provided locator
            for i in range(1, 4):
                self.keyword.check(getattr(practice_site_locators, f"RADIO_BUTTON_XPATH_{i}"))
                time.sleep(1)
        except Exception as e:
            # Handle any exceptions that occur during the selection
            print(f"Error selecting radio button: {e}")
            raise

    def input_text_in_sample_field(self, text):
        try:
            self.keyword.custom_input_text_if_fully_loaded(practice_site_locators.CLASS_EXAMPLE_XPATH, text)
        except Exception as e:
            print(f"Error inputting text in sample field: {e}")
            raise

    def perform_dropdown_selection(self):
        try:
            for i in range(1, 4):
                self.keyword.select_option(getattr(practice_site_locators, "DROPDOWN_XPATH"), f"Option{i}")
                time.sleep(1)
        except Exception as e:
            print(f"Error performing dropdown selection: {e}")
            raise

    def perform_checkbox_selection(self):
        try:
            for i in range(1, 4):
                self.keyword.check(getattr(practice_site_locators, f"CHECKBOX_XPATH_{i}"))
                time.sleep(1)
        except Exception as e:
            print(f"Error performing checkbox selection: {e}")
            raise

    def perform_scroll_to_element(self):
        try:
            self.keyword.scroll_to_element(practice_site_locators.CLASS_EXAMPLE_XPATH)
        except Exception as e:
            print(f"Error performing scroll to element: {e}")
            raise

    def perform_mouse_over(self):
        try:
            self.keyword.mouse_over(practice_site_locators.MOUSE_HOVER_XPATH)
        except Exception as e:
            print(f"Error performing mouse over: {e}")
            raise

    def perform_click_on_over_element(self):
        try:
            self.keyword.click_element(practice_site_locators.MOUSE_HOVER_TOP_XPATH)
        except Exception as e:
            print(f"Error performing click on element: {e}")
            raise