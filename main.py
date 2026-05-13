import time
import random

from notifier import notify
from check_vfs import check_vfs


def check_country(country):
    try:
        result = check_vfs(country)

        if result:
            message = f"🚨 {country.upper()} UPDATE:\n"

            if result["added"]:
                message += f"\n✅ Added:\n{result['added']}\n"

            if result["removed"]:
                message += f"\n❌ Removed:\n{result['removed']}\n"

            notify(message)

            print(f"{country}: change detected")

        else:
            print(f"{country}: no change")

    except Exception as e:
        print(f"{country} error:", e)


countries = ["france", "italy", "spain", "netherlands"]

for country in countries:
    check_country(country)
    time.sleep(random.randint(4, 8))
