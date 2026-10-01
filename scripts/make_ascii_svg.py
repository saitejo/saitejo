from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS = 100
FONT_SIZE = 9
CHAR_W = 5.4
CHAR_H = 11.0
FILL = "#b0b0b0"
BG = "#0d1117"
CURSOR = "#58a6ff"
PAD = 10


def main():
    img = Image.open("source-prepped.png").convert("L")
    w, h = img.size
    rows = int(COLS * (h / w) * 0.55)
    img = img.resize((COLS, rows), Image.LANCZOS)
    pixels = list(img.getdata())

    grid = []
    for r in range(rows):
        line = ""
        for c in range(COLS):
            b = pixels[r * COLS + c]
            idx = int((255 - b) / 255 * (len(RAMP) - 1))
            line += RAMP[idx]
        grid.append(line)

    svg_w = COLS * CHAR_W + PAD * 2
    svg_h = rows * CHAR_H + PAD * 2
    total_time = 2.5
    row_stagger = total_time / rows
    wipe_dur = 0.12

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_w:.1f}" height="{svg_h:.1f}" '
        f'viewBox="0 0 {svg_w:.1f} {svg_h:.1f}">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
    parts.append("<defs>")

    for i in range(rows):
        y = PAD + i * CHAR_H
        begin = i * row_stagger
        parts.append(f'<clipPath id="r{i}">')
        parts.append(
            f'<rect x="{PAD}" y="{y:.1f}" width="0" height="{CHAR_H}">'
        )
        parts.append(
            f'<animate attributeName="width" from="0" '
            f'to="{COLS * CHAR_W:.1f}" begin="{begin:.4f}s" '
            f'dur="{wipe_dur}s" fill="freeze"/>'
        )
        parts.append("</rect>")
        parts.append("</clipPath>")

    parts.append("</defs>")

    for i, line in enumerate(grid):
        y = PAD + i * CHAR_H + FONT_SIZE
        escaped = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        parts.append(
            f'<text clip-path="url(#r{i})" x="{PAD}" y="{y:.1f}" '
            f"font-family=\"'Courier New',monospace\" "
            f'font-size="{FONT_SIZE}px" fill="{FILL}" '
            f'xml:space="preserve">{escaped}</text>'
        )

    for i in range(rows):
        y = PAD + i * CHAR_H
        begin = i * row_stagger
        parts.append(
            f'<rect x="{PAD}" y="{y:.1f}" width="4" '
            f'height="{CHAR_H}" fill="{CURSOR}" opacity="0">'
        )
        parts.append(
            f'<animate attributeName="opacity" '
            f'values="0;0.9;0.9;0" keyTimes="0;0.01;0.99;1" '
            f'begin="{begin:.4f}s" dur="{wipe_dur + 0.05}s" fill="freeze"/>'
        )
        parts.append(
            f'<animate attributeName="x" from="{PAD}" '
            f'to="{PAD + COLS * CHAR_W:.1f}" '
            f'begin="{begin:.4f}s" dur="{wipe_dur}s" fill="freeze"/>'
        )
        parts.append("</rect>")

    parts.append("</svg>")

    with open("sai-ascii.svg", "w") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    main()
