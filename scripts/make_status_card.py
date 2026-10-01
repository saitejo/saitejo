import os

BG = "#0d1117"
TITLE_BG = "#161b22"
BORDER = "#30363d"
ACCENT = "#58a6ff"
TEXT = "#e6edf3"
DIM = "#8b949e"
KEY_COLORS = [
    "#7ee787", "#79c0ff", "#ffa657",
    "#d2a8ff", "#ff7b72", "#58a6ff",
]
FONT = "'JetBrains Mono','Courier New',monospace"
FONT_SIZE = 12.5
LINE_H = 21
WIDTH = 460
HEADER_H = 34
PAD_X = 20
PAD_Y = 16
STATIC = os.environ.get("STATIC") == "1"

WINDOW_TITLE = "session \u2014 sai@system"
PROMPT = "sai@system ~ $ sysctl --status"
SEPARATOR = "\u2500" * 38

ENTRIES = [
    ("Systems", "Distributed Backends, Linux"),
    ("AI / ML", "Deep Learning, LLM Agents, RAG"),
    ("Toolbox", "Docker, CMake, OpenFOAM, Neovim"),
    ("DSA", "Competitive Programming, Graphs"),
    ("Simulation", "Fluid Dynamics (CFD), CAD"),
    ("Status", "\u25cf Online \u00b7 Researching & Building"),
]


def main():
    total_lines = 2 + len(ENTRIES)
    content_h = PAD_Y * 2 + total_lines * LINE_H
    height = HEADER_H + content_h

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}">'
    )
    parts.append(
        f'<rect width="100%" height="100%" rx="9" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1"/>'
    )
    parts.append(
        f'<path d="M 0,9 Q 0,0 9,0 L {WIDTH-9},0 Q {WIDTH},0 {WIDTH},9 L {WIDTH},{HEADER_H} L 0,{HEADER_H} Z" '
        f'fill="{TITLE_BG}"/>'
    )
    parts.append(
        f'<line x1="0" y1="{HEADER_H}" x2="{WIDTH}" y2="{HEADER_H}" '
        f'stroke="{BORDER}" stroke-width="1"/>'
    )
    parts.append('<circle cx="18" cy="17" r="5" fill="#ff5f56"/>')
    parts.append('<circle cx="34" cy="17" r="5" fill="#ffbd2e"/>')
    parts.append('<circle cx="50" cy="17" r="5" fill="#27c93f"/>')
    parts.append(
        f'<text x="{WIDTH // 2}" y="21" text-anchor="middle" '
        f'font-family="{FONT}" font-size="11px" fill="{DIM}">{WINDOW_TITLE}</text>'
    )

    if not STATIC:
        parts.append("<style>")
        for i in range(total_lines):
            delay = 0.5 + i * 0.12
            parts.append(
                f".line{i} {{ opacity: 0; "
                f"animation: fadeIn 0.4s {delay:.2f}s forwards; }}"
            )
        parts.append(
            "@keyframes fadeIn "
            "{ from { opacity: 0; } to { opacity: 1; } }"
        )
        parts.append("</style>")

    y = HEADER_H + PAD_Y + 12
    cls = f' class="line0"' if not STATIC else ""
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-family="{FONT}" '
        f'font-size="{FONT_SIZE}px" fill="{ACCENT}" '
        f'font-weight="bold"{cls}>{PROMPT}</text>'
    )

    y += LINE_H
    cls = f' class="line1"' if not STATIC else ""
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-family="{FONT}" '
        f'font-size="{FONT_SIZE}px" fill="{DIM}"{cls}>{SEPARATOR}</text>'
    )

    for i, (key, val) in enumerate(ENTRIES):
        y += LINE_H
        line_idx = i + 2
        color = KEY_COLORS[i % len(KEY_COLORS)]
        cls = f' class="line{line_idx}"' if not STATIC else ""
        escaped_key = key.replace("&", "&amp;")
        escaped_val = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        parts.append(
            f'<text x="{PAD_X}" y="{y}" font-family="{FONT}" '
            f'font-size="{FONT_SIZE}px"{cls}>'
        )
        parts.append(
            f'<tspan fill="{color}" font-weight="bold">{escaped_key}</tspan>'
        )
        parts.append(f'<tspan fill="{DIM}"> ~ </tspan>')
        parts.append(f'<tspan fill="{TEXT}">{escaped_val}</tspan>')
        parts.append("</text>")

    parts.append("</svg>")

    with open("status-card.svg", "w") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    main()
