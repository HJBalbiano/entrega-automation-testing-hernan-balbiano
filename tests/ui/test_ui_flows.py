from pathlib import Path

import pytest

from tests.ui.pages.cart_page import CartPage
from tests.ui.pages.checkout_overview_page import CheckoutOverviewPage
from tests.ui.pages.checkout_page import CheckoutPage
from tests.ui.pages.inventory_page import InventoryPage
from tests.ui.pages.login_page import LoginPage
from utils.data_loader import load_csv, load_json


DATA_DIR = Path(__file__).parent / "data"
USERS = load_json(DATA_DIR / "users.json")
PRODUCT_SETS = load_json(DATA_DIR / "product_sets.json")
CHECKOUT_DATA = load_csv(DATA_DIR / "checkout_data.csv")


def _first_valid_user():
    return next(user for user in USERS if user.get("valid"))


@pytest.mark.ui
@pytest.mark.parametrize(
    "user",
    [user for user in USERS if user.get("valid")],
    ids=lambda u: u["case"],
)
def test_login_success(driver, base_url, logger, user):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.load(base_url)
    logger.info("Intentando login como %s", user["username"])
    login_page.login(user["username"], user["password"])

    assert inventory_page.on_page(), "El usuario debería ver el inventario tras el login"


@pytest.mark.ui
@pytest.mark.parametrize(
    "user",
    [user for user in USERS if not user.get("valid")],
    ids=lambda u: u["case"],
)
def test_login_negative(driver, base_url, logger, user):
    login_page = LoginPage(driver)

    login_page.load(base_url)
    logger.info("Probando login inválido: %s", user["case"])
    login_page.login(user["username"], user["password"])

    assert user["expected_error"] in login_page.error_message()


@pytest.mark.ui
@pytest.mark.parametrize(
    "product_set",
    PRODUCT_SETS,
    ids=lambda s: s["set"],
)
def test_add_products_to_cart(driver, base_url, logger, product_set):
    user = _first_valid_user()
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.load(base_url)
    login_page.login(user["username"], user["password"])
    logger.info("Añadiendo productos: %s", ", ".join(product_set["products"]))

    for product in product_set["products"]:
        inventory_page.add_to_cart(product)

    inventory_page.open_cart()
    items = cart_page.item_names()
    for product in product_set["products"]:
        assert product in items


@pytest.mark.ui
@pytest.mark.parametrize(
    "checkout_row",
    CHECKOUT_DATA,
    ids=lambda r: f"{r['first']} {r['last']}",
)
def test_checkout_flow(driver, base_url, logger, checkout_row):
    user = _first_valid_user()
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)
    overview_page = CheckoutOverviewPage(driver)

    login_page.load(base_url)
    login_page.login(user["username"], user["password"])
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    inventory_page.open_cart()

    cart_page.proceed_to_checkout()
    checkout_page.fill_form(checkout_row["first"], checkout_row["last"], checkout_row["postal"])
    checkout_page.continue_checkout()

    assert overview_page.on_page(), "Debería mostrarse el resumen antes de finalizar"
    overview_page.finish()
    assert overview_page.success_message() == "THANK YOU FOR YOUR ORDER"


@pytest.mark.ui
def test_remove_item_and_continue_shopping(driver, base_url, logger):
    user = _first_valid_user()
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.load(base_url)
    login_page.login(user["username"], user["password"])
    inventory_page.add_to_cart("Sauce Labs Bolt T-Shirt")
    inventory_page.add_to_cart("Sauce Labs Onesie")
    assert inventory_page.cart_count() == 2

    inventory_page.open_cart()
    cart_page.continue_shopping()
    inventory_page.remove_from_cart("Sauce Labs Onesie")
    assert inventory_page.cart_count() == 1
