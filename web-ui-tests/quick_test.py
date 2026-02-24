from selenium import webdriver
from selenium.webdriver.common.by import By

def test_can_open_page():
    driver = webdriver.Chrome()  # Selenium Manager handles driver
    try:
        driver.get("https://ng12assessor.fanai.dev/")
        assert "NG12 Cancer Risk Assessor" in driver.title
        driver.find_element(By.CSS_SELECTOR, "h1")
    finally:
        driver.quit()