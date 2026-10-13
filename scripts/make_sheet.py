"""Generates the profile drawing sheet (light + dark) as SVG."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])

THEMES = {
    "light": dict(bg="#FBFAF7", ink="#1F2328", muted="#6E7781", faint="#D0D7DE", accent="#C4432B"),
    "dark":  dict(bg="#0D1117", ink="#E6EDF3", muted="#8B949E", faint="#30363D", accent="#F2845C"),
}

SANS = "-apple-system, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

W, H = 1200, 440


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(t):
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    a('<title id="t">Zakaria Tikialine, Software Engineer</title>')
    a('<desc id="d">Profile drawn as an engineering sheet. Frontend, full-stack, AI and data. '
      'Revisions: A, 2025, full-stack intern at NAFTAL. B, 2026, front-end developer at Egor Gaming. '
      'C, 2027, engineering degree at ESTIN. Status: open to freelance.</desc>')
    a(f"""<style>
  .ink{{fill:{t['ink']}}} .mu{{fill:{t['muted']}}} .ac{{fill:{t['accent']}}}
  .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
  .ln{{stroke:{t['ink']};fill:none}} .fl{{stroke:{t['faint']};fill:none}}
  .flow{{stroke:{t['accent']};stroke-width:2;stroke-dasharray:3 9;fill:none;animation:flow 1.6s linear infinite}}
  .pulse{{animation:pulse 2.4s ease-in-out infinite}}
  @keyframes flow{{to{{stroke-dashoffset:-24}}}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
  @media (prefers-reduced-motion: reduce){{.flow,.pulse{{animation:none}}}}
</style>""")
    a(f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
      f'<path d="M0,1 L9,5 L0,9" fill="none" stroke="{t["ink"]}" stroke-width="1.4"/></marker></defs>')

    # paper + frames
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    a('<rect class="ln" x="10.5" y="10.5" width="1179" height="419" stroke-width="1.5"/>')
    a('<rect class="ln" x="30.5" y="30.5" width="1139" height="379" stroke-width="1"/>')

    # zone markers
    col = 1140 / 6
    for i in range(1, 6):
        x = 30.5 + col * i
        a(f'<line class="ln" x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="30" stroke-width="1"/>')
        a(f'<line class="ln" x1="{x:.1f}" y1="410" x2="{x:.1f}" y2="430" stroke-width="1"/>')
    for i in range(6):
        x = 30 + col * (i + 0.5)
        for y in (24, 424):
            a(f'<text class="mono mu" x="{x:.1f}" y="{y}" font-size="10" text-anchor="middle">{i + 1}</text>')
    row = 380 / 3
    for i in range(1, 3):
        y = 30.5 + row * i
        a(f'<line class="ln" x1="10" y1="{y:.1f}" x2="30" y2="{y:.1f}" stroke-width="1"/>')
        a(f'<line class="ln" x1="1170" y1="{y:.1f}" x2="1190" y2="{y:.1f}" stroke-width="1"/>')
    for i, L in enumerate("ABC"):
        y = 30 + row * (i + 0.5) + 4
        for x in (20, 1180):
            a(f'<text class="mono mu" x="{x}" y="{y:.1f}" font-size="10" text-anchor="middle">{L}</text>')

    # identity
    a('<text class="mono ac" x="64" y="84" font-size="12" letter-spacing="3">SOFTWARE ENGINEER</text>')
    a('<text class="sans ink" x="62" y="142" font-size="54" font-weight="600" letter-spacing="-1">Zakaria Tikialine</text>')
    a(f'<text class="sans mu" x="64" y="178" font-size="18">{esc("Frontend & full-stack development  ·  AI & data engineering")}</text>')

    # schematic
    a('<text class="mono mu" x="64" y="244" font-size="10" letter-spacing="2">FIG. A — WHERE I WORK</text>')
    boxes = [("01  INTERFACE", "React · Next.js"), ("02  SERVICES", "Node · Express"),
             ("03  DATA", "PostgreSQL · SQL"), ("04  MODELS", "Python · PyTorch")]
    bw, gap, x0, by, bh = 150, 36, 64, 262, 56
    for i, (lab, val) in enumerate(boxes):
        x = x0 + i * (bw + gap)
        a(f'<rect class="ln" x="{x + .5}" y="{by + .5}" width="{bw}" height="{bh}" stroke-width="1.2"/>')
        a(f'<text class="mono mu" x="{x + 12}" y="{by + 19}" font-size="10" letter-spacing="1.5">{lab}</text>')
        a(f'<text class="sans ink" x="{x + 12}" y="{by + 42}" font-size="15">{esc(val)}</text>')
        if i < 3:
            x1, x2, cy = x + bw + 2, x + bw + gap - 2, by + bh / 2
            a(f'<line class="ln" x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke-width="1.2" marker-end="url(#arr)"/>')
            a(f'<line class="flow" x1="{x1}" y1="{cy + 8}" x2="{x2 - 2}" y2="{cy + 8}"/>')

    # dimension line
    xe = x0 + 4 * bw + 3 * gap
    dy = 356
    for x in (x0 + .5, xe + .5):
        a(f'<line class="fl" x1="{x}" y1="{by + bh + 4}" x2="{x}" y2="{dy + 8}" stroke-width="1" stroke-dasharray="2 3"/>')
    a(f'<line class="ln" x1="{x0 + 2}" y1="{dy}" x2="{xe - 1}" y2="{dy}" stroke-width="1" marker-start="url(#arr)" marker-end="url(#arr)"/>')
    mid = (x0 + xe) / 2
    a(f'<rect x="{mid - 128}" y="{dy - 9}" width="256" height="18" fill="{t["bg"]}"/>')
    a(f'<text class="mono ink" x="{mid}" y="{dy + 4}" font-size="11" letter-spacing="1.5" text-anchor="middle">{esc("END TO END · UI → MODEL")}</text>')

    # revision table
    rx, rw = 820, 326
    a('<text class="mono mu" x="820" y="56" font-size="10" letter-spacing="2">REVISIONS</text>')
    cols = [rx, rx + 44, rx + 120, rx + rw]
    ty = 64
    rows = [("A", "2025.06", "Full-stack intern · NAFTAL", False),
            ("B", "2026.05", "Front-end dev · Egor Gaming", True),
            ("C", "2027", "Engineer's degree · ESTIN", False)]
    a(f'<rect class="ln" x="{rx + .5}" y="{ty + .5}" width="{rw}" height="{22 + 28 * 3}" stroke-width="1"/>')
    a(f'<line class="ln" x1="{rx}" y1="{ty + 22.5}" x2="{rx + rw}" y2="{ty + 22.5}" stroke-width="1"/>')
    for c in cols[1:3]:
        a(f'<line class="ln" x1="{c + .5}" y1="{ty}" x2="{c + .5}" y2="{ty + 22 + 84}" stroke-width="1"/>')
    for i, h in enumerate(("REV", "DATE", "DESCRIPTION")):
        a(f'<text class="mono mu" x="{cols[i] + 10}" y="{ty + 15}" font-size="9" letter-spacing="1.5">{h}</text>')
    for i, (r, d, desc, cur) in enumerate(rows):
        y = ty + 22 + 28 * i
        if i:
            a(f'<line class="fl" x1="{rx}" y1="{y + .5}" x2="{rx + rw}" y2="{y + .5}" stroke-width="1"/>')
        cls = "ac" if cur else "ink"
        a(f'<text class="mono {cls}" x="{cols[0] + 10}" y="{y + 18}" font-size="11">{r}</text>')
        a(f'<text class="mono {cls}" x="{cols[1] + 10}" y="{y + 18}" font-size="11">{d}</text>')
        a(f'<text class="mono {cls}" x="{cols[2] + 10}" y="{y + 18}" font-size="11">{esc(desc)}</text>')

    # title block
    by0 = 232
    rh = [38, 38, 38, 40]
    a(f'<rect class="ln" x="{rx + .5}" y="{by0 + .5}" width="{rw}" height="{sum(rh)}" stroke-width="1.5"/>')
    ys = [by0]
    for h in rh:
        ys.append(ys[-1] + h)
    for y in ys[1:-1]:
        a(f'<line class="ln" x1="{rx}" y1="{y + .5}" x2="{rx + rw}" y2="{y + .5}" stroke-width="1"/>')
    half = rx + rw / 2
    a(f'<line class="ln" x1="{half + .5}" y1="{ys[2]}" x2="{half + .5}" y2="{ys[3]}" stroke-width="1"/>')
    third = rw / 3
    for k in (1, 2):
        a(f'<line class="ln" x1="{rx + third * k + .5:.1f}" y1="{ys[3]}" x2="{rx + third * k + .5:.1f}" y2="{ys[4]}" stroke-width="1"/>')

    def cell(x, y, label, value, cls="ink", dot=False):
        a(f'<text class="mono mu" x="{x + 10}" y="{y + 13}" font-size="9" letter-spacing="1.5">{label}</text>')
        vx = x + 10
        if dot:
            a(f'<circle class="ac pulse" cx="{vx + 4}" cy="{y + 27}" r="4"/>')
            vx += 14
        a(f'<text class="sans {cls}" x="{vx}" y="{y + 31}" font-size="14">{esc(value)}</text>')

    cell(rx, ys[0], "DISCIPLINE", "Software Engineering")
    cell(rx, ys[1], "SPECIALTY", "Frontend · Full-stack · AI & Data")
    cell(rx, ys[2], "LOCATION", "Algeria")
    cell(half, ys[2], "STATUS", "Open to freelance", dot=True)
    cell(rx, ys[3] + 1, "DRAWN BY", "Z. Tikialine")
    cell(rx + third, ys[3] + 1, "REV", "B", cls="ac")
    cell(rx + third * 2, ys[3] + 1, "SHEET", "01 / 01")

    a('</svg>')
    return "\n".join(o)


for name, t in THEMES.items():
    (OUT / f"sheet-{name}.svg").write_text(build(t), encoding="utf-8")
print("ok")
