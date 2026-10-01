import os

BG = "#0d1117"
TITLE_BG = "#161b22"
BORDER = "#30363d"
ACCENT = "#58a6ff"
TEXT = "#e6edf3"
DIM = "#8b949e"
HIGHLIGHT = "#79c0ff"
HIGHLIGHT_GREEN = "#7ee787"
HIGHLIGHT_GOLD = "#f1e05a"
FONT = "'JetBrains Mono','Courier New',monospace"
FONT_SIZE = 12.5
LINE_H = 22
WIDTH = 860
HEADER_H = 34
PAD_X = 24
PAD_Y = 16
STATIC = os.environ.get("STATIC") == "1"

WINDOW_TITLE = "about.txt \u2014 nano"
PROMPT = "sai@github ~ $ cat about.txt"
SEPARATOR = "\u2500" * 70

LINES = [
    [
        ("Engineering student exploring ", TEXT),
        ("AI/ML", HIGHLIGHT),
        (", ", TEXT),
        ("AI agents", HIGHLIGHT_GREEN),
        (", ", TEXT),
        ("Backend Development", HIGHLIGHT_GOLD),
        (", and software systems.", TEXT),
    ],
    [
        ("Drawn to understanding how systems operate from ", TEXT),
        ("mathematical first principles", HIGHLIGHT),
        (" to build robust tools.", TEXT),
    ],
    [
        ("Focusing heavily on ", TEXT),
        ("Machine Learning foundations", HIGHLIGHT),
        (" and high-performance backend pipelines in ", TEXT),
        ("C++", HIGHLIGHT_GOLD),
        (" and ", TEXT),
        ("Python", HIGHLIGHT_GREEN),
        (".", TEXT),
    ],
    [
        ("Practicing ", TEXT),
        ("Competitive Programming", HIGHLIGHT_GOLD),
        (" for algorithmic problem solving, graph theory, and mathematical rigor.", TEXT),
    ],
    [
        ("Exploring ", TEXT),
        ("Computational Fluid Dynamics (CFD)", HIGHLIGHT_GREEN),
        (" and ", TEXT),
        ("CAD", HIGHLIGHT),
        (" at the intersection of physics and simulation.", TEXT),
    ],
]


def main():
    total_lines = 2 + len(LINES)
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
    parts.append('<circle cx="20" cy="17" r="5" fill="#ff5f56"/>')
    parts.append('<circle cx="36" cy="17" r="5" fill="#ffbd2e"/>')
    parts.append('<circle cx="52" cy="17" r="5" fill="#27c93f"/>')
    parts.append(
        f'<text x="{WIDTH // 2}" y="21" text-anchor="middle" '
        f'font-family="{FONT}" font-size="11px" fill="{DIM}">{WINDOW_TITLE}</text>'
    )

    if not STATIC:
        parts.append("<style>")
        for i in range(total_lines):
            delay = 0.2 + i * 0.12
            parts.append(
                f".ab_line{i} {{ opacity: 0; "
                f"animation: fadeIn 0.4s {delay:.2f}s forwards; }}"
            )
        parts.append(
            "@keyframes fadeIn "
            "{ from { opacity: 0; } to { opacity: 1; } }"
        )
        parts.append("</style>")

    y = HEADER_H + PAD_Y + 12
    cls = f' class="ab_line0"' if not STATIC else ""
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-family="{FONT}" '
        f'font-size="{FONT_SIZE}px" fill="{ACCENT}" '
        f'font-weight="bold"{cls}>{PROMPT}</text>'
    )

    y += LINE_H
    cls = f' class="ab_line1"' if not STATIC else ""
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-family="{FONT}" '
        f'font-size="{FONT_SIZE}px" fill="{DIM}"{cls}>{SEPARATOR}</text>'
    )

    for i, segments in enumerate(LINES):
        y += LINE_H
        line_idx = i + 2
        cls = f' class="ab_line{line_idx}"' if not STATIC else ""
        parts.append(
            f'<text x="{PAD_X}" y="{y}" font-family="{FONT}" '
            f'font-size="{FONT_SIZE}px"{cls}>'
        )
        parts.append(f'<tspan fill="{DIM}">\u25b8 </tspan>')
        for text, color in segments:
            escaped = (
                text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            weight = ' font-weight="bold"' if color != TEXT else ""
            parts.append(f'<tspan fill="{color}"{weight}>{escaped}</tspan>')
        parts.append("</text>")

    parts.append("</svg>")

    with open("about-card.svg", "w") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    main()
