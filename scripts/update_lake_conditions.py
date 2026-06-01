import json
import re
from datetime import datetime, timezone

import requests

KRMS_URL = "https://www.krmsradio.com/watertemp/wx.html"
AMEREN_URL = "https://www.ameren.com/reliability/generation/hydro/reports/osage/headwatertailwater"


def get_water_temp():
    html = requests.get(KRMS_URL, timeout=30).text

    m = re.search(
        r"Water Temperature.*?<b>\s*([0-9.]+)",
        html,
        re.I | re.S,
    )

    if not m:
        raise Exception("Could not find water temperature")

    return round(float(m.group(1)))


def get_ameren_data():
    html = requests.get(
        AMEREN_URL,
        timeout=30,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }
    ).text

    if "659." in html:
        print("FOUND TABLE DATA")
    else:
        print("NO TABLE DATA")

    print(html[:10000])

    raise Exception("Debug stop")


def calculate_trend(current_level):
    try:
        with open("lake_conditions.json", "r", encoding="utf-8") as f:
            previous = json.load(f)

        previous_level = float(previous["lakeLevel"])

        if current_level > previous_level + 0.05:
            return "up"

        if current_level < previous_level - 0.05:
            return "down"

        return "flat"

    except Exception:
        return "flat"


water_temp = get_water_temp()
lake_level, discharge = get_ameren_data()
trend = calculate_trend(lake_level)

data = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "waterTemp": water_temp,
    "lakeLevel": round(lake_level, 2),
    "discharge": discharge,
    "trend": trend,
}

with open("lake_conditions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))
