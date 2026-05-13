from playwright.sync_api import sync_playwright
import hashlib
import json

URLS = {
    "france": "https://visa.vfsglobal.com/are/en/fra/book-an-appointment",
    "italy": "https://visa.vfsglobal.com/dxb/en/ita/book-an-appointment"
}

def get_page_hash(html):
    return hashlib.md5(html.encode()).hexdigest()

def check_vfs(country):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URLS[country], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)

        html = page.content().lower()
        browser.close()

        current_hash = get_page_hash(html)

        # ✅ Load previous state
        with open("state.json", "r") as f:
            state = json.load(f)

        key = f"{country}_hash"
        previous_hash = state.get(key, "")

        # ✅ Compare hashes
        if previous_hash == "":
            # First run → just store
            state[key] = current_hash
            with open("state.json", "w") as f:
                json.dump(state, f)
            return False

        if current_hash != previous_hash:
            # ✅ CHANGE DETECTED
            state[key] = current_hash
            with open("state.json", "w") as f:
                json.dump(state, f)
            return True

        return False
