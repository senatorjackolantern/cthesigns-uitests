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
            EC.visibility_of_element_located(By.CSS_SELECTOR, css)
        )

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
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

    def wait_for_either(self, locator_a, locator_b, timeout=10, label_a="A", label_b="B"):
        """
        Waits until either locator_a OR locator_b is present+displayed.
        Returns label_a or label_b.
        On timeout, raises AssertionError with diagnostics.
        """
        last_counts = {"a": 0, "b": 0}

        def either_condition(driver):
            a = driver.find_elements(*locator_a)
            b = driver.find_elements(*locator_b)

            last_counts["a"] = len(a)
            last_counts["b"] = len(b)

            if a and a[0].is_displayed():
                return label_a
            if b and b[0].is_displayed():
                return label_b
            return False

        try:
            return WebDriverWait(self.driver, timeout).until(either_condition)
        except Exception:
            # Diagnostics: how many matches exist by the end?
            a = self.driver.find_elements(*locator_a)
            b = self.driver.find_elements(*locator_b)

            def summarize(elements):
                if not elements:
                    return "0 matches"
                e = elements[0]
                return (
                    f"{len(elements)} matches; first: displayed={e.is_displayed()} "
                    f"enabled={e.is_enabled()} tag={e.tag_name} text={e.text[:80]!r}"
                )

            self.driver.save_screenshot("failure_wait_for_either.png")

            raise AssertionError(
                "Timed out waiting for either state.\n"
                f"Locator A: {locator_a} -> {summarize(a)}\n"
                f"Locator B: {locator_b} -> {summarize(b)}\n"
                "Saved screenshot: failure_wait_for_either.png"
            )

    def wait_for_spinner_to_disappear(self, css, timeout=10):
        def gone(driver):
            return len(driver.find_elements(By.CSS_SELECTOR, css)) == 0
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, css))
        )

    def wait_for_patient_id_error(self, timeout=10):
        return self.wait_visible(self.PATIENT_ID_ERROR, timeout)

    def click_assess(self):
        btn = self.wait_clickable(self.ASSESS_BUTTON)
        btn.click()

    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click_submit_chat(self):
        btn = self.wait_clickable(self.CHAT_SEND_BUTTON)
        btn.click()
