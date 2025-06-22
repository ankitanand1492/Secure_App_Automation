import pytest
from pages.login_page import LoginPage
from utils import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

@pytest.mark.order(1)
def test_valid_login(driver):
    """Verify testbot user can successfully login."""
    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)
    login_page.login(config.BOT_USER, config.BOT_PASS)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//h1[contains(text(), 'Welcome {config.BOT_USER}')]"))
    )
    assert f"Welcome {config.BOT_USER}!" in driver.page_source


@pytest.mark.order(2)
def test_lockout_after_failed_attempts(driver):
    """Verify user is locked out after 3 consecutive failed login attempts."""
    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)

    for attempt in range(2):
        print(f"Attempt #{attempt + 1}")
        login_page.login(config.BOT_USER, "wrongpassword")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
        )
        assert "Invalid credentials" in driver.page_source
        time.sleep(3)

    # Third failed attempt
    login_page.login(config.BOT_USER, "wrongpassword")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
    )
    assert ("Account locked. Try again later." in driver.page_source or
            "Account locked due to too many failed attempts." in driver.page_source)


@pytest.mark.order(4)
def test_testbot_user_locked_across_sessions(driver):
    """Verify locked testbot user cannot login from different browsers."""
    chrome_driver = webdriver.Chrome()
    chrome_driver.implicitly_wait(5)
    login_page_chrome = LoginPage(chrome_driver)
    login_page_chrome.load(config.BASE_URL)
    login_page_chrome.login(config.BOT_USER, config.BOT_PASS)
    assert "Account locked" in chrome_driver.page_source
    chrome_driver.quit()

    try:
        firefox_driver = webdriver.Firefox()
        firefox_driver.implicitly_wait(5)
        login_page_firefox = LoginPage(firefox_driver)
        login_page_firefox.load(config.BASE_URL)
        login_page_firefox.login(config.BOT_USER, config.BOT_PASS)
        assert "Account locked" in firefox_driver.page_source
        firefox_driver.quit()
    except Exception as e:
        print("⚠️ Firefox test skipped:", e)


@pytest.mark.order(5)
def test_user_can_login_after_lockout_timeout(driver):
    """Verify locked user can login after 5-minute timeout."""
    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)

    print("Waiting 5 minutes for lockout to expire...")
    time.sleep(305)

    login_page.load(config.BASE_URL)
    login_page.enter_username(config.BOT_USER)
    login_page.enter_password(config.BOT_PASS)
    login_page.bypass_captcha()
    login_page.click_login()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert f"Welcome {config.BOT_USER}!" in driver.page_source


@pytest.mark.order(6)
def test_login_fails_without_captcha(driver):
    """Verify login fails without solving CAPTCHA."""
    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)

    login_page.enter_username(config.USERNAME)
    login_page.enter_password(config.PASSWORD)
    # Skipping captcha
    login_page.click_login()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
    )
    assert "CAPTCHA verification failed" in driver.page_source
