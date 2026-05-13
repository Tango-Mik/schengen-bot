from playwright.sync_api import sync_playwright

URLS = {
    "france": "https://visa.vfsglobal.com/are/en/fra/book-an-appointment",
    "italy": "https://visa.vfsglobal.com/dxb/en/ita/book-an-appointment"
}

def check_vfs(country):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URLS[country], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)

        html = page.content().lower()
        browser.close()

        # ✅ Common "no slots" indicators
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

        # ✅ EXTRA: Italy-specific safeguard
        if country == "italy":
            if "welcome to vfs global" in html:
                return False
            if "apply for a visa" in html:
                return False
            if "book an appointment" in html:
                return False

        # ✅ EXTRA: France safeguard
        if country == "france":
            if "book an appointment" in html:
                return False

        return True


# TEMP TEST
print("France:", check_vfs("france"))
print("Italy:", check_vfs("italy"))