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

# ✅ CLEAN + EXTRACT
def extract_content(html):
    html = html.lower()

    # remove noise blocks
    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    parts = []
    parts += re.findall(r"<h[1-6].*?>(.*?)</h[1-6]>", html)
    parts += re.findall(r"<button.*?>(.*?)</button>", html)
    parts += re.findall(r"<p.*?>(.*?)</p>", html)
    parts += re.findall(r"<a.*?>(.*?)</a>", html)

    content = " ".join(parts)

    # ✅ REMOVE COOKIES / PRIVACY / GENERIC UI
    noise = [
        "cookie","privacy","consent","gdpr","preference",
        "accept","reject","policy","terms","conditions"
    ]

    for n in noise:
        content = content.replace(n, "")

    content = re.sub(r"\s+", " ", content)
    return content.strip()


# ✅ PRIORITY DETECTION
def detect_priority(text):
    HIGH = [
        "appointment available",
        "select date",
        "calendar",
        "book now",
        "schedule",
        "choose date"
    ]

    MEDIUM = [
        "appointment",
        "book appointment",
        "start application",
        "continue",
        "login"
    ]

    for k in HIGH:
        if k in text:
            return "HIGH"

    for k in MEDIUM:
        if k in text:
            return "MEDIUM"

    return "LOW"


# ✅ DIFF (SAFE + LIMITED)
def generate_diff(old, new):
    diff = list(difflib.ndiff(old.split(), new.split()))

    added = [w[2:] for w in diff if w.startswith('+ ') and len(w) > 2]
    removed = [w[2:] for w in diff if w.startswith('- ') and len(w) > 2]

    return " ".join(added[:12]), " ".join(removed[:12])


# ✅ MAIN CHECK
def check_vfs(country):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URLS[country], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)

        html = page.content()
        browser.close()

        current = extract_content(html)

        with open("state.json", "r") as f:
            state = json.load(f)

        key = f"{country}_content"
        previous = state.get(key, "")

        # baseline
        if previous == "":
            state[key] = current
            json.dump(state, open("state.json", "w"))
            return None

        # compare
        if current != previous:
            added, removed = generate_diff(previous, current)

            state[key] = current
            json.dump(state, open("state.json", "w"))

            if not added and not removed:
                return None

            combined = f"{added} {removed}"
            priority = detect_priority(combined)

            return {
                "added": added,
                "removed": removed,
                "priority": priority
            }

        return None
