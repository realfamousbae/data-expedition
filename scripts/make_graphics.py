#!/usr/bin/env python3
"""Generate the README graphics (assets/cards*.svg, assets/workflow*.svg).

Usage:
    python scripts/make_graphics.py

Plain SVG with no external fonts or scripts, so the files render the same on
GitHub in light and dark themes. Every graphic sits on its own dark card.
Texts live in the STRINGS table below: edit them here, then regenerate.
"""

from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG = "#0b0f0c"
CARD = "#111a13"
BORDER = "#23422b"
GREEN = "#55c23a"
GREEN_DIM = "#2f6b22"
TEXT = "#e9f1ea"
MUTED = "#93a99a"
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

STRINGS = {
    "en": {
        "cards": [
            ("Workspace", ["Architecture and data flow", "Audits: security, deps, drift", "Git history, logs, datasets"]),
            ("Web", ["Archives, primary documents", "Registries, filings, forums", "Deep but public pages"]),
            ("Verify", ["Verdict for every claim", "Independent corroboration", "Calibrated confidence"]),
            ("Report", ["Bottom line first", "path:line and dated URLs", "Coverage and honest limits"]),
        ],
        "steps": ["Frame", "Depth tier", "Map", "Explore", "Ledger", "Verify", "Saturate", "Self-audit", "Report"],
        "loop": "iterate until saturated",
        "workflow_title": "From question to evidence-backed answer",
    },
    "ru": {
        "cards": [
            ("Workspace", ["Архитектура и потоки данных", "Аудиты кода и зависимостей", "История git, логи, данные"]),
            ("Web", ["Архивы и первоисточники", "Реестры, отчётность, форумы", "Глубины публичного веба"]),
            ("Проверка", ["Вердикт по каждому факту", "Независимые источники", "Калиброванная уверенность"]),
            ("Отчёт", ["Сначала вывод", "path:line и URL с датой", "Покрытие и честные пределы"]),
        ],
        "steps": ["Рамка", "Глубина", "Карта", "Поиск", "Журнал", "Проверка", "Насыщение", "Самоаудит", "Отчёт"],
        "loop": "повторять до насыщения",
        "workflow_title": "От вопроса до ответа с доказательствами",
    },
}


def t(x, y, text, size=13, fill=TEXT, weight="400", anchor="start", family=FONT):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(text)}</text>')


def icon(kind, cx, cy):
    """Simple 28px line icons drawn around (cx, cy)."""
    s = f'fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    if kind == 0:  # node graph
        return (f'<g {s}><circle cx="{cx}" cy="{cy-9}" r="4"/><circle cx="{cx-10}" cy="{cy+9}" r="4"/>'
                f'<circle cx="{cx+10}" cy="{cy+9}" r="4"/><path d="M{cx-2} {cy-5} L{cx-8} {cy+5} M{cx+2} {cy-5} L{cx+8} {cy+5}"/></g>')
    if kind == 1:  # globe
        return (f'<g {s}><circle cx="{cx}" cy="{cy}" r="13"/><ellipse cx="{cx}" cy="{cy}" rx="6" ry="13"/>'
                f'<path d="M{cx-13} {cy} H{cx+13}"/></g>')
    if kind == 2:  # shield + check
        return (f'<g {s}><path d="M{cx} {cy-14} L{cx+12} {cy-9} V{cy+2} C{cx+12} {cy+9} {cx+6} {cy+13} {cx} {cy+15} '
                f'C{cx-6} {cy+13} {cx-12} {cy+9} {cx-12} {cy+2} V{cy-9} Z"/><path d="M{cx-5} {cy+1} L{cx-1} {cy+5} L{cx+6} {cy-4}"/></g>')
    # document
    return (f'<g {s}><path d="M{cx-9} {cy-14} H{cx+3} L{cx+10} {cy-7} V{cy+14} H{cx-9} Z"/>'
            f'<path d="M{cx-4} {cy} H{cx+5} M{cx-4} {cy+6} H{cx+5}"/></g>')


def cards_svg(lang):
    cards = STRINGS[lang]["cards"]
    w, h, cw, gap, pad = 1000, 214, 240, 8, 12
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="Workspace, Web, Verify, Report">',
           f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>']
    x0 = (w - (4 * cw + 3 * gap)) / 2
    for i, (title, lines) in enumerate(cards):
        x = x0 + i * (cw + gap)
        out.append(f'<rect x="{x}" y="{pad+2}" width="{cw}" height="{h-2*pad-4}" rx="12" fill="{CARD}" stroke="{BORDER}"/>')
        out.append(f'<circle cx="{x+40}" cy="{pad+52}" r="24" fill="#16261a" stroke="{GREEN_DIM}"/>')
        out.append(icon(i, x + 40, pad + 52))
        out.append(t(x + 76, pad + 59, title, size=20, weight="700"))
        for j, line in enumerate(lines):
            y = pad + 102 + j * 25
            out.append(f'<circle cx="{x+24}" cy="{y-4}" r="2.6" fill="{GREEN}"/>')
            mono = ":" in line and "path" in line
            out.append(t(x + 36, y, line, size=12 if mono else 13.5, fill=MUTED, family=MONO if mono else FONT))
    out.append("</svg>")
    return "\n".join(out)


def workflow_svg(lang):
    d = STRINGS[lang]
    steps = d["steps"]
    n = len(steps)
    w, h = 1000, 214
    left, right = 62, w - 62
    step = (right - left) / (n - 1)
    cy = 126
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="{escape(" > ".join(steps))}">',
           f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>',
           t(w / 2, 34, d["workflow_title"], size=15, fill=MUTED, weight="600", anchor="middle"),
           f'<line x1="{left}" y1="{cy}" x2="{right}" y2="{cy}" stroke="{GREEN_DIM}" stroke-width="2"/>']
    xs = [left + i * step for i in range(n)]
    # iterate arc from Verify (index 5) back to Explore (index 3)
    a, b = xs[5], xs[3]
    out.append(f'<path d="M{a} {cy-24} C{a} {cy-62} {b} {cy-62} {b} {cy-24}" fill="none" stroke="{GREEN}" '
               f'stroke-width="1.6" stroke-dasharray="4 4"/>')
    out.append(f'<path d="M{b-4} {cy-31} L{b} {cy-24} L{b+5} {cy-31}" fill="none" stroke="{GREEN}" stroke-width="1.6" '
               f'stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(t((a + b) / 2, cy - 62, d["loop"], size=11.5, fill=GREEN, anchor="middle"))
    for i, (x, label) in enumerate(zip(xs, steps)):
        last = i == n - 1
        out.append(f'<circle cx="{x}" cy="{cy}" r="19" fill="{GREEN if last else CARD}" stroke="{GREEN}" stroke-width="2"/>')
        out.append(t(x, cy + 5.5, str(i + 1), size=15, fill=BG if last else GREEN, weight="700", anchor="middle"))
        out.append(t(x, cy + 50, label, size=13.5, fill=TEXT, weight="600", anchor="middle"))
    out.append("</svg>")
    return "\n".join(out)


def main():
    ASSETS.mkdir(exist_ok=True)
    for lang, suffix in (("en", ""), ("ru", ".ru")):
        (ASSETS / f"cards{suffix}.svg").write_text(cards_svg(lang), encoding="utf-8")
        (ASSETS / f"workflow{suffix}.svg").write_text(workflow_svg(lang), encoding="utf-8")
        print(f"wrote assets/cards{suffix}.svg and assets/workflow{suffix}.svg")


if __name__ == "__main__":
    main()
