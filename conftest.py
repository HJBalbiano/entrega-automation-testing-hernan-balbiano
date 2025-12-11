from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from utils.data_loader import ensure_dir
from utils.driver_factory import create_chrome_driver
from utils.logger import create_logger


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Base URL para pruebas de UI",
    )


@pytest.fixture(scope="session")
def base_url(request) -> str:
    return request.config.getoption("--base-url")


@pytest.fixture
def logger(request):
    test_name = request.node.name
    log_file = Path("artifacts") / "logs" / f"{test_name}.log"
    return create_logger(test_name, log_file=str(log_file))


@pytest.fixture
def driver(request):
    driver = create_chrome_driver()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.failed and "driver" in item.funcargs:
        driver = item.funcargs["driver"]
        screenshots_dir = ensure_dir(Path("artifacts") / "screenshots")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{item.name}_{timestamp}.png"
        screenshot_path = screenshots_dir / file_name
        driver.save_screenshot(str(screenshot_path))

        html = item.config.pluginmanager.getplugin("html")
        if html:
            extra = getattr(rep, "extra", [])
            extra.append(html.extras.png(str(screenshot_path), mime_type="image/png"))
            rep.extra = extra
