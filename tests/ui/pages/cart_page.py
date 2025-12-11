from selenium.webdriver.common.by import By

from tests.ui.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BTN = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")

    def item_names(self):
        return [el.text for el in self.elements(self.ITEM_NAME)]

    def proceed_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BTN)

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING_BTN)
