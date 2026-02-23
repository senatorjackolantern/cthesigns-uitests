from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_clickable_css(self, css, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(("css selector", css))
        )

    def wait_visible_css(self, css, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(("css selector", css))
        )

    def click_button_text(self, text, timeout=10):
        xpath = f"//button[normalize-space()='{text}']"
        button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()

