from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Base page with common helpers."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def click(self, locator: tuple[str, str]) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: tuple[str, str], text: str) -> None:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator: tuple[str, str]) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def elements(self, locator: tuple[str, str]):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
