from playwright.sync_api import sync_playwright

URLS = {
    "france": "https://visa.vfsglobal.com/are/en/fra/book-an-appointment",
    "italy": "https://visa.vfsglobal.com/dxb/en/ita/book-an-appointment"
}

def check_vfs(country):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URLS[country], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(10000)

        html = page.content().lower()
        browser.close()

        blocked_phrases = [
            "no appointment",
            "fully booked",
            "no slots",
            "currently unavailable",
            "no available",
            "try again later"
        ]

        for phrase in blocked_phrases:
            if phrase in html:
                return False

        # ✅ Always assume NO slots unless very sure
        return False
