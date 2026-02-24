from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class HomePage(BasePage):
    PRIMARY_CTA = "[data-tab='assess']"
    ASSESS_SUCCESS = (By.CSS_SELECTOR, "div.result-card")
    ASSESS_ERROR = (By.CSS_SELECTOR, "div.error-card") 
    ASSESS_BUTTON = (By.CSS_SELECTOR, "button#assess-btn")
    PATIENT_ID_INPUT = (By.CSS_SELECTOR, "input#patient-id")
    PATIENT_ID_ERROR = (By.CSS_SELECTOR, "div.error-card")
    CHAT_TAB_BUTTON = (By.CSS_SELECTOR, "[data-tab='chat']")
    NEW_CHAT_BUTTON = (By.CSS_SELECTOR, "button.new-chat-btn")
    CHAT_TEXT_INPUT = (By.CSS_SELECTOR, "textarea#chat-input")
    CHAT_SEND_BUTTON = (By.CSS_SELECTOR, "button#chat-send-btn")
    CHAT_MESSAGES = (By.CSS_SELECTOR, "div#chat-messages")
    CHAT_MESSAGE_ITEMS = (By.CSS_SELECTOR, "#chat-messages > *")


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

    def enter_chat_text(self, value, timeout=10):
        field = self.wait_visible(self.CHAT_TEXT_INPUT)
        field.clear()
        field.send_keys(str(value))
        return self

    def click_send_chat(self, timeout=10):
        self.wait_clickable(self.CHAT_SEND_BUTTON, timeout=timeout).click()
        return self

    def send_chat_message(self, value, timeout=10):
        self.enter_chat_text(value)
        self.click_send_chat()
        return self

    def wait_for_chat_response(self, timeout=20):
        def messages_exist(driver):
            msgs = driver.find_elements(*self.CHAT_MESSAGE_ITEMS)
            return len(msgs) > 0

        WebDriverWait(self.driver, timeout).until(messages_exist)

    def chat_message_count(self):
        return len(self.driver.find_elements(*self.CHAT_MESSAGE_ITEMS))

    def wait_for_chat_messages_added(self, before_count, added=2, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.find_elements(*self.CHAT_MESSAGE_ITEMS)) >= before_count + added
        )

    def wait_for_last_chat_message_text(self, min_chars=40, timeout=60):
        def ready(driver):
            items = driver.find_elements(*self.CHAT_MESSAGE_ITEMS)
            if not items:
                return False
            txt = items[-1].text.strip()
            return len(txt) >= min_chars

        WebDriverWait(self.driver, timeout).until(ready)