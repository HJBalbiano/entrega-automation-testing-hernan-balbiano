from selenium.webdriver.common.by import By

from tests.ui.pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def on_page(self) -> bool:
        return self.is_visible(self.INVENTORY_CONTAINER)

    def _slug(self, product_name: str) -> str:
        return product_name.lower().replace(" ", "-")

    def add_to_cart(self, product_name: str) -> None:
        button_locator = (By.CSS_SELECTOR, f"[data-test='add-to-cart-{self._slug(product_name)}']")
        self.click(button_locator)

    def remove_from_cart(self, product_name: str) -> None:
        button_locator = (By.CSS_SELECTOR, f"[data-test='remove-{self._slug(product_name)}']")
        self.click(button_locator)

    def open_cart(self) -> None:
        self.click(self.CART_ICON)

    def listed_products(self):
        return [el.text for el in self.elements(self.ITEM_NAME)]

    def cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0
