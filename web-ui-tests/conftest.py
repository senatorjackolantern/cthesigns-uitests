import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("UI_BASE_URL", "https://ng12assessor.fanai.dev/")

@pytest.fixture
def driver():
    options = Options()

    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1400,900")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)  # prefer explicit waits, not implicit
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            driver.save_screenshot("failure.png")