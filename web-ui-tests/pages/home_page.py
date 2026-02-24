from .base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    PRIMARY_CTA = "[data-tab='assess']"
    ASSESS_SUCCESS = (By.CSS_SELECTOR, "div.result-card")
    ASSESS_ERROR = (By.CSS_SELECTOR, ".error") # not sure what the actual error state looks like but this can easily be updated to match

    def open(self, url):
        self.driver.get(url)
        return self

    def primary_cta(self):
        return self.wait_clickable_css(self.PRIMARY_CTA)