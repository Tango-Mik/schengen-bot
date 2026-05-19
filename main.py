import time
import random
from notifier import notify
from check_vfs import check_vfs
from check_tls import check_germany_tls

PRIORITY_ICONS = {
    "HIGH": "🔴",
    "MEDIUM": "🟡",
    "LOW": "🟢"
}

# ✅ avoid duplicate spam per run cycle
already_alerted = set()

def should_notify(country, priority):
    key = f"{country}_{priority}"
    if key in already_alerted:
        return False

    # ✅ suppress LOW repetition
    if priority == "LOW":
        return False

    already_alerted.add(key)
    return True


def check_country(country):
    try:
        result = check_vfs(country)

        if result:
            priority = result.get("priority", "LOW")

            if not should_notify(country, priority):
                print(f"{country}: suppressed ({priority})")
                return

            icon = PRIORITY_ICONS.get(priority, "🟢")

            msg = f"{icon} {country.upper()} ({priority})\n"

            if result.get("added"):
                msg += f"\n+ {result['added']}"

            if result.get("removed"):
                msg += f"\n- {result['removed']}"

            notify(msg)
            print(f"{country}: ALERT ({priority})")

        else:
            print(f"{country}: no change")

    except Exception as e:
        print(f"{country} error:", e)


def check_germany():
    try:
        result = check_germany_tls()

        if result:
            msg = "🚨 GERMANY TLS CHANGE\n"

            if result.get("added"):
                msg += f"\n+ {result['added']}"

            if result.get("removed"):
                msg += f"\n- {result['removed']}"

            notify(msg)
            print("germany: ALERT")

        else:
            print("germany: no change")

    except Exception as e:
        print("germany error:", e)


countries = ["france", "italy", "spain", "netherlands"]

for c in countries:
    check_country(c)
    time.sleep(random.randint(4, 8))

time.sleep(random.randint(4, 8))
check_germany()
