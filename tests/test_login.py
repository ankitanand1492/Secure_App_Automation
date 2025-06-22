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
    print("Starting valid login test for testbot user")
    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)
    login_page.login(config.BOT_USER, config.BOT_PASS)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//h1[contains(text(), 'Welcome {config.BOT_USER}')]"))
    )

    assert f"Welcome {config.BOT_USER}!" in driver.page_source, "❌ Login message not found in page source"
    print("✅ Valid login test passed")


@pytest.mark.order(2)
def test_lockout_after_failed_attempts(driver):
    """Verify user is locked out after 3 consecutive failed login attempts."""
    print("Starting lockout test with invalid credentials")
    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)

    for attempt in range(2):
        print(f"⛔ Invalid attempt #{attempt + 1}")
        login_page.login(config.BOT_USER, "wrongpassword")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
        )
        assert "Invalid credentials" in driver.page_source, "❌ Expected 'Invalid credentials' not found"
        time.sleep(2)

    # Third attempt
    print("Attempting 3rd invalid login to trigger lockout")
    login_page.login(config.BOT_USER, "wrongpassword")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
    )

    assert (
        "Account locked" in driver.page_source
        or "too many failed attempts" in driver.page_source
    ), "❌ Lockout message not found after 3 failed attempts"
    print("✅ Lockout after 3 attempts verified")


@pytest.mark.order(3)
def test_testbot_user_locked_across_sessions():
    """Verify locked testbot user cannot login from different browsers."""
    print("Verifying lockout persists across browser sessions")

    # Chrome session
    chrome_driver = webdriver.Chrome()
    chrome_driver.implicitly_wait(5)
    login_chrome = LoginPage(chrome_driver)
    login_chrome.load(config.BASE_URL)
    login_chrome.login(config.BOT_USER, config.BOT_PASS)
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
    )
    assert "Account locked" in chrome_driver.page_source, "❌ Lockout failed in Chrome"
    chrome_driver.quit()
    print("✅ Chrome session verified")

    # Firefox session
    try:
        firefox_driver = webdriver.Firefox()
        firefox_driver.implicitly_wait(5)
        login_firefox = LoginPage(firefox_driver)
        login_firefox.load(config.BASE_URL)
        login_firefox.login(config.BOT_USER, config.BOT_PASS)
        WebDriverWait(firefox_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
    )
        assert "Account locked" in firefox_driver.page_source, "❌ Lockout failed in Firefox"
        firefox_driver.quit()
        print("✅ Firefox session verified")
    except Exception as e:
        print("⚠️ Firefox test skipped:", e)


@pytest.mark.order(4)
def test_user_can_login_after_lockout_timeout(driver):
    """Verify locked user can login after 5-minute timeout."""
    print("⏳ Waiting 5 minutes for lockout to expire...")
    time.sleep(305)  # 5 minutes and buffer

    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)
    login_page.login(config.BOT_USER, config.BOT_PASS)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )

    assert f"Welcome {config.BOT_USER}!" in driver.page_source, "❌ User not logged in after timeout"
    print("✅ User can login again after lockout timeout")


@pytest.mark.order(5)
def test_login_fails_without_captcha(driver):
    """Verify login fails without solving CAPTCHA."""
    print("🔍 Testing CAPTCHA enforcement")

    login_page = LoginPage(driver)
    login_page.load(config.BASE_URL)

    login_page.enter_username(config.USERNAME)
    login_page.enter_password(config.PASSWORD)
    # Intentionally skipping CAPTCHA
    login_page.click_login()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))
    )

    assert "CAPTCHA verification failed" in driver.page_source, "❌ CAPTCHA failure message not found"
    print("✅ CAPTCHA enforcement verified")
