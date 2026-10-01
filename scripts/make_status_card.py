import os

BG = "#0d1117"
BORDER = "#30363d"
ACCENT = "#58a6ff"
TEXT = "#e6edf3"
DIM = "#8b949e"
KEY_COLORS = [
    "#7ee787", "#79c0ff", "#ffa657",
    "#d2a8ff", "#ff7b72", "#58a6ff",
]
FONT = "'JetBrains Mono','Courier New',monospace"
FONT_SIZE = 13
LINE_H = 22
PAD = 24
WIDTH = 460
STATIC = os.environ.get("STATIC") == "1"

TITLE = "sai@system ~ (session: live)"
SEPARATOR = "\u2500" * len(TITLE)

ENTRIES = [
    ("Systems", "Distributed Backends, Linux Kernel"),
    ("AI / ML", "Deep Learning, LLM Agents, RAG"),
    ("Toolbox", "Docker, CMake, OpenFOAM, Neovim"),
    ("Problem Solving", "Competitive Programming, Graph Theory"),
    ("Simulation", "Fluid Dynamics (CFD), CAD"),
    ("Status", "\u25cf Online \u00b7 Researching & Building"),
]


def main():
    total_lines = 2 + len(ENTRIES)
    height = PAD * 2 + total_lines * LINE_H + 16

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}">'
    )
    parts.append(
        f'<rect width="100%" height="100%" rx="8" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1"/>'
    )

    if not STATIC:
        parts.append("<style>")
        for i in range(total_lines):
            delay = 0.8 + i * 0.15
            parts.append(
                f".line{i} {{ opacity: 0; "
                f"animation: fadeIn 0.4s {delay:.2f}s forwards; }}"
            )
        parts.append(
            "@keyframes fadeIn "
            "{ from { opacity: 0; } to { opacity: 1; } }"
        )
        parts.append("</style>")

    y = PAD + FONT_SIZE
    cls = f' class="line0"' if not STATIC else ""
    parts.append(
        f'<text x="{PAD}" y="{y}" font-family="{FONT}" '
        f'font-size="{FONT_SIZE}px" fill="{ACCENT}" '
        f'font-weight="bold"{cls}>{TITLE}</text>'
    )

    y += LINE_H
    cls = f' class="line1"' if not STATIC else ""
    parts.append(
        f'<text x="{PAD}" y="{y}" font-family="{FONT}" '
        f'font-size="{FONT_SIZE}px" fill="{DIM}"{cls}>{SEPARATOR}</text>'
    )

    for i, (key, val) in enumerate(ENTRIES):
        y += LINE_H
        line_idx = i + 2
        color = KEY_COLORS[i % len(KEY_COLORS)]
        cls = f' class="line{line_idx}"' if not STATIC else ""
        parts.append(
            f'<text x="{PAD}" y="{y}" font-family="{FONT}" '
            f'font-size="{FONT_SIZE}px"{cls}>'
        )
        parts.append(
            f'<tspan fill="{color}" font-weight="bold">{key}</tspan>'
        )
        parts.append(f'<tspan fill="{DIM}"> ~ </tspan>')
        parts.append(f'<tspan fill="{TEXT}">{val}</tspan>')
        parts.append("</text>")

    parts.append("</svg>")

    with open("status-card.svg", "w") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    main()
