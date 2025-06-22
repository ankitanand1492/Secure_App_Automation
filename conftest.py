import pytest
import os
import base64
import datetime
from py.xml import html  # ✅ Fix for html tag usage
from pytest_html import extras  # ✅ For screenshot extras
from utils.driver_factory import get_driver
from utils.warm_up import warm_up_app
from utils import config

# Automatically warm up the app before tests
@pytest.fixture(scope="session", autouse=True)
def warm_up():
    warm_up_app(config.BASE_URL)

# Setup browser driver fixture
@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

# Configure pytest-html plugin globally
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin('html')

# Add "Description" column to report header
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))  # ✅ Fix applied

# Add test case docstring to the report table
@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(getattr(report, "description", "No description")))  # ✅ Fix applied

# Capture screenshots on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__) if item.function.__doc__ else "No description"

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            file_name = f"{item.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(path)

            with open(path, "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode("utf-8")
            extra = getattr(report, 'extra', [])
            extra.append(extras.image(f"data:image/png;base64,{encoded_img}", mime_type="image/png"))
            report.extra = extra
