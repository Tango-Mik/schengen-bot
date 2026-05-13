from playwright.sync_api import sync_playwright
import hashlib
import json
import re

URLS = {
    "france": "https://visa.vfsglobal.com/are/en/fra/book-an-appointment",
    "italy": "https://visa.vfsglobal.com/dxb/en/ita/book-an-appointment",
    "spain": "https://visa.vfsglobal.com/are/en/esp/book-an-appointment",
    "netherlands": "https://visa.vfsglobal.com/are/en/nld/book-an-appointment"
}

# ✅ Extract only meaningful visible content
def extract_important_content(html):

    html = html.lower()

    # remove scripts
    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)

    # remove styles
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)

    # remove comments
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    important = []

    # ✅ headings
    important += re.findall(r"<h[1-6].*?>(.*?)</h[1-6]>", html)

    # ✅ buttons
    important += re.findall(r"<button.*?>(.*?)</button>", html)

    # ✅ links
    important += re.findall(r"<a.*?>(.*?)</a>", html)

    # ✅ paragraphs
    important += re.findall(r"<p.*?>(.*?)</p>", html)

    content = " ".join(important)

    # clean whitespace
    content = re.sub(r"\s+", " ", content)

    return content.strip()


def get_hash(content):
    return hashlib.md5(content.encode()).hexdigest()


def check_vfs(country):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URLS[country], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)

        html = page.content()
        browser.close()

        # ✅ Filter important content only
        filtered = extract_important_content(html)

        current_hash = get_hash(filtered)

        # ✅ Load state
        with open("state.json", "r") as f:
            state = json.load(f)

        key = f"{country}_hash"
        previous_hash = state.get(key, "")

        # ✅ First run → baseline
        if previous_hash == "":
            state[key] = current_hash
            with open("state.json", "w") as f:
                json.dump(state, f)
            return False

        # ✅ Detect meaningful change
        if current_hash != previous_hash:
            state[key] = current_hash
            with open("state.json", "w") as f:
                json.dump(state, f)
            return True

        return False
