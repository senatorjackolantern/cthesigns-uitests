from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


def test_homepage_has_primary_cta(driver, base_url):
    page = HomePage(driver).open(base_url)
    page.click_button_text("Patient Assessment")


def test_homepage_has_chat_assistant(driver, base_url):
    page = HomePage(driver).open(base_url)  
    page.click_button_text("Chat")

def test_patient_assessment(driver, base_url):
    page = HomePage(driver).open(base_url)
    page.click_button_text("Patient Assessment")
    page.wait_for_spinner_to_disappear(".loading-spinner")
    page.click_button_text("PT-101 (John Doe)")
    page.wait_for_spinner_to_disappear(".loading-spinner")
    result = page.wait_for_either(
        HomePage.ASSESS_SUCCESS,
        HomePage.ASSESS_ERROR
    )

    assert result == "A", "Assessment ended in error state"