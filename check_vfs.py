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

        initial_url = page.url
        html = page.content().lower()

        # ✅ STEP 1: strong NO-slot detection
        blocked = [
            "no appointment",
            "fully booked",
            "no slots",
            "currently unavailable",
            "try again later"
        ]
        for b in blocked:
            if b in html:
                browser.close()
                return False

        # ✅ STEP 2: try clicking ANY booking-related button
        try:
            buttons = page.locator("button")
            count = buttons.count()

            for i in range(count):
                text = buttons.nth(i).inner_text().lower()

                if "book" in text or "appointment" in text:
                    try:
                        buttons.nth(i).click(timeout=3000)
                        page.wait_for_timeout(5000)

                        new_url = page.url
                        new_html = page.content().lower()

                        # ✅ If page changes → strong signal
                        if new_url != initial_url:
                            browser.close()
                            return True

                        # ✅ If login / appointment page detected
                        if "login" in new_html or "calendar" in new_html:
                            browser.close()
                            return True

                    except:
                        continue

        except:
            pass

        browser.close()
        return False
