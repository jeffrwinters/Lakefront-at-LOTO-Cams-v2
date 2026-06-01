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
    html = requests.get(AMEREN_URL, timeout=30).text

    print("HTML LENGTH:", len(html))
    print("HEADWATER FOUND:", "Headwater" in html)
    print("TAILWATER FOUND:", "Tailwater" in html)
    print("DISCHARGE FOUND:", "Discharge" in html)
    print("REPORT FOUND:", "658." in html)

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
