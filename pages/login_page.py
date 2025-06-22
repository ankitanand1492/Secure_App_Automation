from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.login_button = (By.CLASS_NAME, "btn.btn-primary")
        self.captcha_script = "document.getElementById('g-recaptcha-response').innerHTML = 'PASSED'"

    def load(self, url):
        self.driver.get(url)

    def enter_username(self, username):
        username_field = self.wait.until(EC.visibility_of_element_located(self.username_input))
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.wait.until(EC.visibility_of_element_located(self.password_input))
        password_field.clear()
        password_field.send_keys(password)

    def bypass_captcha(self):
        self.driver.execute_script(self.captcha_script)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
        login_btn.click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.bypass_captcha()
        self.click_login()
