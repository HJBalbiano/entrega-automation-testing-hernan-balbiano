import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def create_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """Create a Chrome driver using Selenium Manager to resolve the binary."""
    options = ChromeOptions()
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    if headless or os.getenv("HEADLESS", "1") == "1":
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(6)
    return driver
