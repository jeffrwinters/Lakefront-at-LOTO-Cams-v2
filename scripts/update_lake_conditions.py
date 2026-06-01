import json
import re
from datetime import datetime, timezone

import requests

KRMS_URL = "https://www.krmsradio.com/watertemp/wx.html"
AMEREN_URL = "https://www.ameren.com/reliability/generation/hydro/reports/osage/headwatertailwater"

def get_water_temp():
html = requests.get(KRMS_URL, timeout=30).text

```
m = re.search(
    r'Water Temperature.*?<b>\s*([0-9.]+)',
    html,
    re.I | re.S
)

if not m:
    raise Exception("Could not find water temperature")

return round(float(m.group(1)))
```

def get_ameren_data():
html = requests.get(AMEREN_URL, timeout=30).text

```
print("HTML LENGTH:", len(html))
print(html[:5000])

raise Exception("Debug stop")
```
