import requests
from bs4 import BeautifulSoup
import json
import os
import re

USERNAME = "saitejo"
URL = f"https://github.com/users/{USERNAME}/contributions"


def main():
    resp = requests.get(URL, headers={"Accept": "text/html"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    cells = soup.select("td.ContributionCalendar-day")

    for cell in cells:
        date = cell.get("data-date")
        level = int(cell.get("data-level", "0"))
        if not date:
            continue

        count = 0
        tip = cell.find("tool-tip")
        if tip:
            text = tip.get_text(strip=True)
        else:
            span = cell.find("span", class_="sr-only")
            text = span.get_text(strip=True) if span else ""

        m = re.search(r"(\d+)\s+contribution", text)
        if m:
            count = int(m.group(1))

        days.append({"date": date, "level": level, "count": count})

    days.sort(key=lambda d: d["date"])

    total = sum(d["count"] for d in days)

    streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            streak += 1
        else:
            break

    longest = 0
    current = 0
    for d in days:
        if d["count"] > 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(
            {
                "username": USERNAME,
                "total": total,
                "days": days,
                "current_streak": streak,
                "longest_streak": longest,
                "best_day": {
                    "date": best["date"],
                    "count": best["count"],
                },
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
