from .base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    PRIMARY_CTA = "[data-tab='assess']"
    ASSESS_SUCCESS = (By.CSS_SELECTOR, "div.result-card")
    ASSESS_ERROR = (By.CSS_SELECTOR, "div.error-card") 
    ASSESS_BUTTON = (By.CSS_SELECTOR, "button#assess-btn")
    PATIENT_ID_INPUT = (By.CSS_SELECTOR, "input#patient-id")
    PATIENT_ID_ERROR = (By.CSS_SELECTOR, "div.error-card")
    CHAT_TAB_BUTTON = "[data-tab='chat']"
    NEW_CHAT_BUTTON = (By.CSS_SELECTOR, "button.new-chat-btn")


    def open(self, url):
        self.driver.get(url)
        return self

    def primary_cta(self):
        return self.wait_clickable_css(self.PRIMARY_CTA)

    def enter_patient_id(self, value):
        field = self.wait_visible(self.PATIENT_ID_INPUT)
        field.clear()
        field.send_keys(str(value))

    def go_to_chat(self):
        self.wait_clickable(self.CHAT_TAB_BUTTON).click()
        return self

    def wait_for_chat_loaded(self, timeout=10):
        return self.wait_visible(self.NEW_CHAT_BUTTON, timeout=timeout)