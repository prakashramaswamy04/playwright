"""Locators and URLs for the Rahul Shetty Academy practice site."""

PRACTICE_SITE_URL = "https://rahulshettyacademy.com/AutomationPractice/"
RADIO_BUTTON_XPATH_1 = "//input[@value='radio1']"
RADIO_BUTTON_XPATH_2 = "//input[@value='radio2']"
RADIO_BUTTON_XPATH_3 = "//input[@value='radio3']"

CLASS_EXAMPLE_XPATH = "//input[@id='autocomplete']"

DROPDOWN_XPATH = "//select[@id='dropdown-class-example']"
CHECKBOX_XPATH_1 = "//input[@id='checkBoxOption1']"
CHECKBOX_XPATH_2 = "//input[@id='checkBoxOption2']"
CHECKBOX_XPATH_3 = "//input[@id='checkBoxOption3']"

MOUSE_HOVER_EXAMPLE_XPATH = "//legend[text()='Mouse Hover Example']"

MOUSE_HOVER_XPATH = "//button[@id='mousehover']"
MOUSE_HOVER_TOP_XPATH = "//div[@class='mouse-hover-content']/a[text()='Top']"
MOUSE_HOVER_REFRESH_XPATH = "//div[@class='mouse-hover-content']/a[text()='Reload']"

WEB_TABLE_XPATH = "//legend[text()='Web Table Example']"
WEB_TABLE_ROW_XPATH = "//table[@id='product' and @name='courses']/tbody/tr"
WEB_TABLE_COLUMN_NAME_XPATH = "//table[@id='product' and @name='courses']/tbody/tr[{i}]/th[{j}]"
WEB_TABLE_CELL_XPATH = "//table[@id='product' and @name='courses']/tbody/tr[{i}]/td[{j}]"

WEB_TABLE_FIXED_HEADER_XPATH = "//div[@class='tableFixHead']//table[@id='product']/tbody/tr"
WEB_TABLE_FIXED_HEADER_COLUMN_NAME_XPATH = "//div[@class='tableFixHead']//table[@id='product']/thead/tr[{i}]/th[{j}]"
WEB_TABLE_FIXED_HEADER_CELL_XPATH = "//div[@class='tableFixHead']//table[@id='product']/tbody/tr[{i}]/td[{j}]"

WEB_TABLE_DATA_CSV_PATH = "./first_playwright_code/test_data/csv_files/web_table_data_{}.csv"
WEB_TABLE_FIXED_HEADER_DATA_CSV_PATH = "./first_playwright_code/test_data/csv_files/web_table_fixed_header_data_{}.csv"