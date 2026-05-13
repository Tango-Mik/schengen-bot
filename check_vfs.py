from playwright.sync_api import sync_playwright
import hashlib
import json
import re
import difflib

URLS = {
    "france": "https://visa.vfsglobal.com/are/en/fra/book-an-appointment",
    "italy": "https://visa.vfsglobal.com/dxb/en/ita/book-an-appointment",
    "spain": "https://visa.vfsglobal.com/are/en/esp/book-an-appointment",
    "netherlands": "https://visa.vfsglobal.com/are/en/nld/book-an-appointment"
}

# ✅ Extract meaningful content
def extract_content(html):
    html = html.lower()
    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    important = []
    important += re.findall(r"<h[1-6].*?>(.*?)</h[1-6]>", html)
    important += re.findall(r"<button.*?>(.*?)</button>", html)
    important += re.findall(r"<a.*?>(.*?)</a>", html)
    important += re.findall(r"<p.*?>(.*?)</p>", html)

    content = " ".join(important)
    content = re.sub(r"\s+", " ", content)

    return content.strip()


# ✅ Generate readable diff
def generate_diff(old, new):
    old_words = old.split()
    new_words = new.split()

    diff = list(difflib.ndiff(old_words, new_words))

    added = [w[2:] for w in diff if w.startswith('+ ')]
    removed = [w[2:] for w in diff if w.startswith('- ')]

    added_text = " ".join(added[:20])   # limit size
    removed_text = " ".join(removed[:20])

    return added_text, removed_text


def check_vfs(country):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URLS[country], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)

        html = page.content()
        browser.close()

        current_content = extract_content(html)

        # ✅ Load state
        with open("state.json", "r") as f:
            state = json.load(f)

        key_content = f"{country}_content"
        previous_content = state.get(key_content, "")

        # ✅ First run
        if previous_content == "":
            state[key_content] = current_content
            with open("state.json", "w") as f:
                json.dump(state, f)
            return None

        # ✅ Detect change
        if current_content != previous_content:
            added, removed = generate_diff(previous_content, current_content)

            state[key_content] = current_content
            with open("state.json", "w") as f:
                json.dump(state, f)

            return {
                "added": added,
                "removed": removed
            }

        return None
