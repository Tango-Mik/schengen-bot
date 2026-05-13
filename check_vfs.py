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

        # ✅ Strong NO-slot signals
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

        # ✅ Smart signal: check if "book" button exists and is enabled
        try:
            buttons = page.locator("button")
            count = buttons.count()

            for i in range(count):
                text = buttons.nth(i).inner_text().lower()
                if "book" in text:
                    if buttons.nth(i).is_enabled():
                        browser.close()
                        return True
        except:
            pass

        browser.close()
        return False
