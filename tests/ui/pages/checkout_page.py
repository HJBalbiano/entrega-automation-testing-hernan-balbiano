from selenium.webdriver.common.by import By

from tests.ui.pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_form(self, first: str, last: str, postal: str) -> None:
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)

    def continue_checkout(self) -> None:
        self.click(self.CONTINUE_BTN)

    def error_message(self) -> str:
        return self.get_text(self.ERROR)
