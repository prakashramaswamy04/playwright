from first_playwright_code.keywords.common import Common
from first_playwright_code.page_locators import practice_site_locators

class FramePage(Common):
    def __init__(self, keyword: Common):
        self.keyword = keyword

    def select_frame_from_web(self, frame_locator: str) -> None:
        """Select a frame using the given frame locator."""
        self.keyword.select_frame(frame_locator)
        print(f"Selected frame: {frame_locator}")

    