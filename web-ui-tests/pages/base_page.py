from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ButtonDisabledError(AssertionError):
    pass


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_visible_css(self, css, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css))
        )

    def click_button_text(self, text, timeout=10):
        xpath = f"//button[normalize-space()='{text}']"
        wait = WebDriverWait(self.driver, timeout)

        # 1 — ensure button exists
        try:
            el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            raise AssertionError(f"Button with text '{text}' was not found on the page")

        # 2 — visible?
        if not el.is_displayed():
            self.driver.save_screenshot("failure_not_visible.png")
            raise AssertionError(f"Button '{text}' exists but is not visible")

        # 3 — disabled detection
        disabled_attr = el.get_attribute("disabled")
        aria_disabled = el.get_attribute("aria-disabled")
        classes = el.get_attribute("class") or ""

        if (
            disabled_attr is not None
            or aria_disabled == "true"
            or "pointer-events-none" in classes
        ):
            self.driver.save_screenshot("failure_disabled.png")
            raise ButtonDisabledError(
                f"Button '{text}' is present but disabled. "
                f"(disabled={disabled_attr}, aria-disabled={aria_disabled}, classes='{classes}')"
            )

        # 4 — scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", el
        )

        # 5 — clickable
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            self.driver.save_screenshot("failure_not_clickable.png")
            raise AssertionError(
                f"Button '{text}' never became clickable (likely overlay/spinner)"
            )

        el.click()
