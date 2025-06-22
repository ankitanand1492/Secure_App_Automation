from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    # Commenting out headless so browser is visible
    # options.add_argument("--headless")
    
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver
