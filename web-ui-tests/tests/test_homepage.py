from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


def test_homepage_has_primary_cta(driver, base_url):
    page = HomePage(driver).open(base_url)
    page.click_button_text("🔍 Assess Patient")


def test_homepage_has_chat_assistant(driver, base_url):
    page = HomePage(driver).open(base_url)  
    page.click_button_text("💬 Chat Assistant")