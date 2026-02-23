from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage

def test_homepage_has_primary_cta(driver):
    page = HomePage(driver).open("http://localhost:5173/")
    page.click_button_text("🔍 Assess Patient")
    page.click_button_text("💬 Chat Assistant")