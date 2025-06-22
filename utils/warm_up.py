# utils/warm_up.py
import requests
import time

def warm_up_app(url, retries=6, delay=10):
    for attempt in range(retries):
        try:
            print(f"🌐 Warming up the app... attempt {attempt + 1}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ App is awake and responding!")
                return True
        except Exception as e:
            print(f"⚠️ App not ready yet: {e}")
        time.sleep(delay)
    print("❌ App did not respond after retries.")
    return False
