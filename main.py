import time
import random

from notifier import notify
from check_vfs import check_vfs
from check_tls import check_germany_tls


# ✅ Priority icons
PRIORITY_ICONS = {
    "HIGH": "🔴",
    "MEDIUM": "🟡",
    "LOW": "🟢"
}


# ✅ Handle VFS countries
def check_country(country):
    try:
        result = check_vfs(country)

        if result:
            priority = result.get("priority", "LOW")
            icon = PRIORITY_ICONS.get(priority, "🟢")

            message = f"{icon} {country.upper()} UPDATE ({priority} PRIORITY):\n"

            # ✅ Added content
            if result.get("added"):
                message += f"\n✅ Added:\n{result['added']}\n"

            # ✅ Removed content
            if result.get("removed"):
                message += f"\n❌ Removed:\n{result['removed']}\n"

            notify(message)
            print(f"{country}: change detected ({priority})")

        else:
            print(f"{country}: no change")

    except Exception as e:
        print(f"{country} error:", e)


# ✅ Handle Germany (TLS)
def check_germany():
    try:
        result = check_germany_tls()

        if result:
            # Germany currently does not have priority logic
            message = "🚨 GERMANY (TLS) UPDATE:\n"

            if result.get("added"):
                message += f"\n✅ Added:\n{result['added']}\n"

            if result.get("removed"):
                message += f"\n❌ Removed:\n{result['removed']}\n"

            notify(message)
            print("germany: change detected")

        else:
            print("germany: no change")

    except Exception as e:
        print("germany error:", e)


# ✅ Countries list
vfs_countries = ["france", "italy", "spain", "netherlands"]


# ✅ Run all VFS checks
for country in vfs_countries:
    check_country(country)
    time.sleep(random.randint(4, 8))  # avoid detection


# ✅ Run Germany check separately
time.sleep(random.randint(4, 8))
check_germany()
