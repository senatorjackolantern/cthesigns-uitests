from .base_page import BasePage

class HomePage(BasePage):
    PRIMARY_CTA = "[data-testid='primary-cta']"

    def open(self, url):
        self.driver.get(url)
        return self

    def primary_cta(self):
        return self.wait_clickable_css(self.PRIMARY_CTA)