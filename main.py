import time
import random

from notifier import notify
from check_vfs import check_vfs

# ✅ Track current state (prevents spam)
state = {
    "france": "no_slots",
    "italy": "no_slots"
}

def check_country(country):
    try:
        available = check_vfs(country)

        if available and state[country] == "no_slots":
            notify(f"🚨 CHANGE DETECTED on {country.upper()} booking page!")
            state[country] = "slots_available"

        if not available:
            state[country] = "no_slots"

        print(f"{country}: {state[country]}")

    except Exception as e:
        print(f"{country} error:", e)


# ✅ Run checks
check_country("france")
time.sleep(random.randint(4, 8))
check_country("italy")
