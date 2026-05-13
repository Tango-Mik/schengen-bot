from playwright.sync_api import sync_playwright
import json
import re
import difflib

TLS_URL = "https://visa-de.tlscontact.com/ae/dxb/index.php"

# ✅ Extract meaningful content
def extract_content(html):
    html = html.lower()

    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)

    important = []
    important += re.findall(r"<h[1-6].*?>(.*?)</h[1-6]>", html)
    important += re.findall(r"<button.*?>(.*?)</button>", html)
    important += re.findall(r"<p.*?>(.*?)</p>", html)
    important += re.findall(r"<a.*?>(.*?)</a>", html)

    return " ".join(important).strip()


# ✅ Generate diff
def generate_diff(old, new):
    diff = list(difflib.ndiff(old.split(), new.split()))

    added = [w[2:] for w in diff if w.startswith('+ ')]
    removed = [w[2:] for w in diff if w.startswith('- ')]

    return " ".join(added[:20]), " ".join(removed[:20])


def check_germany_tls():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(TLS_URL, timeout=60000)
        page.wait_for_timeout(10000)

        html = page.content()
        browser.close()

        content = extract_content(html)

        # ✅ Load state
        with open("state.json", "r") as f:
            state = json.load(f)

        previous = state.get("germany_content", "")

        # ✅ First run
        if previous == "":
            state["germany_content"] = content
            with open("state.json", "w") as f:
                json.dump(state, f)
            return None

        # ✅ Change detected
        if content != previous:
            added, removed = generate_diff(previous, content)

            state["germany_content"] = content
            with open("state.json", "w") as f:
                json.dump(state, f)

            return {
                "added": added,
                "removed": removed
            }

        return None
