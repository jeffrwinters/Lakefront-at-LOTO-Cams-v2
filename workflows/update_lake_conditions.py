import json
from datetime import datetime, timezone

# TODO:
# Replace these placeholder values with real Ameren / lake data sources.
# This script is structured so you only need to update the three values below.

water_temp = 78
lake_level = 659.2
discharge = 31

# Simple trend calculation placeholder.
trend = "flat"

data = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "waterTemp": water_temp,
    "lakeLevel": lake_level,
    "discharge": discharge,
    "trend": trend
}

with open("lake_conditions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("lake_conditions.json updated")
