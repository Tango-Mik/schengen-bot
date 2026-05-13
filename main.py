import time
import random

from notifier import notify
from check_vfs import check_vfs

state_runtime = {
    "france": "no_change",
    "italy": "no_change",
    "spain": "no_change",
    "netherlands": "no_change"
}

def check_country(country):
    try:
        changed = check_vfs(country)

        if changed and state_runtime[country] == "no_change":
            message = f"🚨 IMPORTANT: Change detected on {country.upper()} booking page!"
            notify(message)
            state_runtime[country] = "changed"

        if not changed:
            state_runtime[country] = "no_change"

        print(f"{country}: {state_runtime[country]}")

    except Exception as e:
        print(f"{country} error:", e)


countries = ["france", "italy", "spain", "netherlands"]

for country in countries:
    check_country(country)
    time.sleep(random.randint(4, 8))
``import time
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
