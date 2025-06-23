# 🔐 Secure App Automation Suite

This repository contains an automated test suite using **Selenium + Pytest** to validate the secure login flow for a Flask-based web application. It covers:

- Valid login with CAPTCHA
- Lockout after 3 failed attempts
- Lockout validation across browsers
- Unlock after timeout
- CAPTCHA validation failure
- Multi-browser support

---

Cold Start Warning:
When you run the automation test suite for the first time, it might take up to 60 seconds to execute due to the cold start of the application under test (e.g., warming up the server or launching dependencies).
Subsequent runs should execute significantly faster.


## 🚀 Quick Start (No Virtualenv)

### 1. 📥 Clone the Repo

```bash
git clone https://github.com/ankitanand1492/Secure_App_Automation.git
cd Secure_App_Automation
```

### 2. 🧩 Install Dependencies

Make sure Python (3.8+) and pip are installed.

```bash
pip install -r requirements.txt
```

### 3. 🧪 Run Tests

```bash
pytest --html=reports/report.html
```

---

## 📦 Features

| Feature                         | Status |
|-------------------------------|--------|
| Valid login flow              | ✅     |
| Lockout after 3 failures      | ✅     |
| Lockout across browsers       | ✅     |
| Login retry after 5 mins      | ✅     |
| CAPTCHA verification check    | ✅     |
| Beautiful HTML report         | ✅     |

---

## ⚙️ Project Structure

```
Secure_App_Automation/
│
├── pages/                     # Page Object Model
│   └── login_page.py
│
├── tests/                     # Test cases
│   └── test_login.py
│
├── utils/                     # Config, Driver, Warm-up utilities
│   ├── config.py
│   ├── driver_factory.py
│   └── warm_up.py
│
├── reports/                   # HTML test reports and screenshots
│
├── conftest.py                # Pytest fixtures & reporting hooks
├── requirements.txt
└── README.md
```

---

## 🧰 Requirements

- Python 3.8+
- Google Chrome installed
- (Optional) Firefox installed for cross-browser tests

> **Note**: You don’t need to manually install ChromeDriver — Selenium Manager handles it automatically (since v4.6+).

---

## 📸 HTML Reports

After test run, check:

```
/reports/report.html
```

Screenshots on failure will be embedded directly into the report.

---

## 🌐 Application Under Test

> URL: [https://secure-login-app-h8e3.onrender.com](https://secure-login-app-h8e3.onrender.com)

---

## 👨‍💻 Author

**Ankit Anand**  
QA Automation Engineer | Python | Selenium | Pytest

---
