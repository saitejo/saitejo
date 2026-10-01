import json
from datetime import datetime, timedelta

PALETTE = [
    "#161b22", "#0e4429", "#006d32",
    "#26a641", "#39d353", "#69f0a0",
]
BOX = 13
GAP = 3
RADIUS = 2
BG = "#0d1117"
TEXT_COLOR = "#8b949e"
FONT = "'Segoe UI','Helvetica Neue',sans-serif"
FONT_SIZE = 11
PAD_TOP = 36
PAD_LEFT = 40
PAD_RIGHT = 20
PAD_BOTTOM = 50
MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def github_row(dt):
    return (dt.weekday() + 1) % 7


def main():
    with open("data/contributions.json") as f:
        data = json.load(f)

    days = data["days"]
    if not days:
        return

    day_map = {d["date"]: d for d in days}

    first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
    last_date = datetime.strptime(days[-1]["date"], "%Y-%m-%d")

    offset = github_row(first_date)
    start_sunday = first_date - timedelta(days=offset)

    total_days = (last_date - start_sunday).days + 1
    num_weeks = (total_days + 6) // 7

    grid_w = num_weeks * (BOX + GAP)
    grid_h = 7 * (BOX + GAP)
    svg_w = PAD_LEFT + grid_w + PAD_RIGHT
    svg_h = PAD_TOP + grid_h + PAD_BOTTOM

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_w}" height="{svg_h}" '
        f'viewBox="0 0 {svg_w} {svg_h}">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
    parts.append("<style>")
    parts.append(
        "@keyframes fadeIn "
        "{ from { opacity: 0; } to { opacity: 1; } }"
    )
    parts.append(
        ".box { opacity: 0; animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards; }"
    )
    parts.append("</style>")

    prev_month = -1
    for wi in range(num_weeks):
        for dow in range(7):
            dt = start_sunday + timedelta(days=wi * 7 + dow)
            if dt < first_date or dt > last_date:
                continue
            if dt.month != prev_month:
                x = PAD_LEFT + wi * (BOX + GAP)
                parts.append(
                    f'<text x="{x}" y="{PAD_TOP - 8}" '
                    f'font-family="{FONT}" font-size="{FONT_SIZE}px" '
                    f'fill="{TEXT_COLOR}">{MONTHS[dt.month - 1]}</text>'
                )
                prev_month = dt.month
                break

    day_labels = {1: "Mon", 3: "Wed", 5: "Fri"}
    for dow, label in day_labels.items():
        y = PAD_TOP + dow * (BOX + GAP) + BOX - 1
        parts.append(
            f'<text x="{PAD_LEFT - 6}" y="{y}" '
            f'font-family="{FONT}" font-size="{FONT_SIZE - 2}px" '
            f'fill="{TEXT_COLOR}" text-anchor="end">{label}</text>'
        )

    for wi in range(num_weeks):
        for dow in range(7):
            dt = start_sunday + timedelta(days=wi * 7 + dow)
            if dt < first_date or dt > last_date:
                continue
            date_str = dt.strftime("%Y-%m-%d")
            row = github_row(dt)
            x = PAD_LEFT + wi * (BOX + GAP)
            y = PAD_TOP + row * (BOX + GAP)
            info = day_map.get(date_str, {"level": 0, "count": 0})
            level = min(info["level"], len(PALETTE) - 1)
            color = PALETTE[level]
            delay = wi * 0.04 + row * 0.015
            parts.append(
                f'<rect class="box" x="{x}" y="{y}" '
                f'width="{BOX}" height="{BOX}" rx="{RADIUS}" '
                f'fill="{color}" '
                f'style="animation-delay:{delay:.3f}s"/>'
            )

    legend_y = PAD_TOP + grid_h + 16
    legend_x = svg_w - PAD_RIGHT - len(PALETTE) * (BOX + GAP) - 60
    parts.append(
        f'<text x="{legend_x}" y="{legend_y + BOX - 2}" '
        f'font-family="{FONT}" font-size="{FONT_SIZE - 2}px" '
        f'fill="{TEXT_COLOR}">Less</text>'
    )
    lx = legend_x + 30
    for i, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{lx + i * (BOX + GAP)}" y="{legend_y}" '
            f'width="{BOX}" height="{BOX}" rx="{RADIUS}" '
            f'fill="{color}"/>'
        )
    parts.append(
        f'<text x="{lx + len(PALETTE) * (BOX + GAP) + 4}" '
        f'y="{legend_y + BOX - 2}" font-family="{FONT}" '
        f'font-size="{FONT_SIZE - 2}px" '
        f'fill="{TEXT_COLOR}">More</text>'
    )

    total = data.get("total", 0)
    parts.append(
        f'<text x="{PAD_LEFT}" y="{legend_y + BOX - 2}" '
        f'font-family="{FONT}" font-size="{FONT_SIZE}px" '
        f'fill="{TEXT_COLOR}">'
        f'{total:,} contributions in the last year</text>'
    )

    parts.append("</svg>")

    with open("contrib-heatmap.svg", "w") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    main()
