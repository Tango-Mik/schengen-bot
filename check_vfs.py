from playwright.sync_api import sync_playwright
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

    # ✅ Remove noise
    noise_keywords = [
        "cookie","privacy","consent","gdpr","preference","accept","reject","policy"
    ]
    for word in noise_keywords:
        content = content.replace(word, "")

    content = re.sub(r"\s+", " ", content)
    return content.strip()


# ✅ PRIORITY DETECTION
def detect_priority(text):
    high_keywords = [
        "appointment available",
        "select date",
        "calendar",
        "book now",
        "schedule"
    ]

    medium_keywords = [
        "appointment",
        "book appointment",
        "start application",
        "continue"
    ]

    for k in high_keywords:
        if k in text:
            return "HIGH"

    for k in medium_keywords:
        if k in text:
            return "MEDIUM"

    return "LOW"


# ✅ DIFF GENERATION
def generate_diff(old, new):
    old_words = old.split()
    new_words = new.split()

    diff = list(difflib.ndiff(old_words, new_words))

    added = [w[2:] for w in diff if w.startswith('+ ') and len(w) > 2]
    removed = [w[2:] for w in diff if w.startswith('- ') and len(w) > 2]

    return " ".join(added[:15]), " ".join(removed[:15])


# ✅ MAIN FUNCTION
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

        key = f"{country}_content"
        previous_content = state.get(key, "")

        # ✅ First run
        if previous_content == "":
            state[key] = current_content
            with open("state.json", "w") as f:
                json.dump(state, f)
            return None

        # ✅ Compare
        if current_content != previous_content:
            added, removed = generate_diff(previous_content, current_content)

            state[key] = current_content
            with open("state.json", "w") as f:
                json.dump(state, f)

            if not added and not removed:
                return None

            combined = (added + " " + removed).strip()
            priority = detect_priority(combined)

            return {
                "added": added,
                "removed": removed,
                "priority": priority
            }

        return None
