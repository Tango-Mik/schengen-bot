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
        page.wait_for_timeout(8000)

        html = page.content().lower()

        # ✅ 1. Strong NO-SLOT signals
        blocked_phrases = [
            "no appointment",
            "fully booked",
            "no slots",
            "currently unavailable",
            "try again later"
        ]

        for phrase in blocked_phrases:
            if phrase in html:
                browser.close()
                return False

        # ✅ 2. SMART SIGNAL: Look for booking button
        try:
            button = page.locator("button:has-text('book')")
            if button.count() > 0:
                # Check if button is enabled
                if button.first.is_enabled():
                    browser.close()
                    return True   # strong positive signal
        except:
            pass

        # ✅ 3. SMART SIGNAL: Navigation change
        current_url = page.url
        if "appointment" in current_url:
