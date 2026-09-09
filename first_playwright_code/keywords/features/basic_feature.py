from first_playwright_code.keywords.pages.basic_page import BasicPage
from first_playwright_code.keywords.common import Common
class BasicFeature:

    def __init__(self, keyword: Common):
        self.basic_page = BasicPage(keyword)

    def perform_basic_action(self):
        try:
            self.basic_page.select_radio_button()
            self.basic_page.input_text_in_sample_field("Sample Text")
            self.basic_page.perform_dropdown_selection()
            self.basic_page.perform_checkbox_selection()
        except Exception as e:
            print(f"Error performing basic action: {e}")
            raise

    def perform_basic_mouse_over(self):
        try:
            self.basic_page.perform_scroll_to_element()
            self.basic_page.perform_mouse_over()
            self.basic_page.perform_click_on_over_element()
        except Exception as e:
            print(f"Error performing basic mouse over: {e}")
            raise
