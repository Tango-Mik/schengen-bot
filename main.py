import time
import random

from notifier import notify
from check_vfs import check_vfs
from check_tls import check_germany_tls


# ✅ Check VFS countries (France, Italy, Spain, Netherlands)
def check_country(country):
    try:
        result = check_vfs(country)

        if result:
            message = f"🚨 {country.upper()} UPDATE:\n"

            # ✅ Show added content
            if result.get("added"):
                message += f"\n✅ Added:\n{result['added']}\n"

            # ✅ Show removed content
            if result.get("removed"):
                message += f"\n❌ Removed:\n{result['removed']}\n"

            notify(message)

            print(f"{country}: change detected")

        else:
            print(f"{country}: no change")

    except Exception as e:
        print(f"{country} error:", e)


# ✅ Check Germany (TLS workaround)
def check_germany():
    try:
        result = check_germany_tls()

        if result:
            message = "🚨 GERMANY (TLS) UPDATE:\n"

            # ✅ Added
            if result.get("added"):
                message += f"\n✅ Added:\n{result['added']}\n"

            # ✅ Removed
            if result.get("removed"):
                message += f"\n❌ Removed:\n{result['removed']}\n"

            notify(message)

            print("germany: change detected")

        else:
            print("germany: no change")

    except Exception as e:
        print("germany error:", e)


# ✅ VFS Countries list
vfs_countries = ["france", "italy", "spain", "netherlands"]


# ✅ Run VFS checks
for country in vfs_countries:
    check_country(country)
    time.sleep(random.randint(4, 8))


# ✅ Run Germany TLS check separately
time.sleep(random.randint(4, 8))
check_germany()
