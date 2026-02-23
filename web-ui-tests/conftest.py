import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()

    # Headless in CI; normal locally unless you want headless always
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1400,900")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)  # prefer explicit waits, not implicit
    yield driver
    driver.quit()

def base_url():
    return os.getenv("BASE_URL", "http://localhost:5173/")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            driver.save_screenshot("failure.png")