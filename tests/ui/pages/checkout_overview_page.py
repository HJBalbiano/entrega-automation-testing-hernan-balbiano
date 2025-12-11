from selenium.webdriver.common.by import By

from tests.ui.pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    SUMMARY_CONTAINER = (By.ID, "checkout_summary_container")
    FINISH_BTN = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def on_page(self) -> bool:
        return self.is_visible(self.SUMMARY_CONTAINER)

    def finish(self) -> None:
        self.click(self.FINISH_BTN)

    def success_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)
