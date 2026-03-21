#!/usr/bin/env python3
"""Render ANSI terminal capture files into simple SVG screenshots."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_FG = '#d0d0d0'
DEFAULT_BG = '#111111'
CELL_W = 8.6
CELL_H = 18
FONT_SIZE = 14
PAD_X = 12
PAD_Y = 12

ANSI16 = {
    30: '#000000', 31: '#aa0000', 32: '#00aa00', 33: '#aa5500',
    34: '#0000aa', 35: '#aa00aa', 36: '#00aaaa', 37: '#aaaaaa',
    90: '#555555', 91: '#ff5555', 92: '#55ff55', 93: '#ffff55',
    94: '#5555ff', 95: '#ff55ff', 96: '#55ffff', 97: '#ffffff',
    40: '#000000', 41: '#aa0000', 42: '#00aa00', 43: '#aa5500',
    44: '#0000aa', 45: '#aa00aa', 46: '#00aaaa', 47: '#aaaaaa',
    100: '#555555', 101: '#ff5555', 102: '#55ff55', 103: '#ffff55',
    104: '#5555ff', 105: '#ff55ff', 106: '#55ffff', 107: '#ffffff',
}

SGR_RE = re.compile(r'\x1b\[([0-9;]*)m')


@dataclass
class Cell:
    char: str
    fg: str = DEFAULT_FG
    bg: str = DEFAULT_BG


def xterm_256_to_hex(index: int) -> str:
    if index < 16:
        lookup = [
            '#000000', '#800000', '#008000', '#808000', '#000080', '#800080', '#008080', '#c0c0c0',
            '#808080', '#ff0000', '#00ff00', '#ffff00', '#0000ff', '#ff00ff', '#00ffff', '#ffffff',
        ]
        return lookup[index]
    if 16 <= index <= 231:
        i = index - 16
        r, g, b = i // 36, (i % 36) // 6, i % 6
        steps = [0, 95, 135, 175, 215, 255]
        return f'#{steps[r]:02x}{steps[g]:02x}{steps[b]:02x}'
    gray = 8 + (index - 232) * 10
    return f'#{gray:02x}{gray:02x}{gray:02x}'


def apply_sgr(params: list[int], fg: str, bg: str) -> tuple[str, str]:
    if not params:
        return DEFAULT_FG, DEFAULT_BG

    i = 0
    while i < len(params):
        p = params[i]
        if p == 0:
            fg, bg = DEFAULT_FG, DEFAULT_BG
        elif p == 39:
            fg = DEFAULT_FG
        elif p == 49:
            bg = DEFAULT_BG
        elif p in ANSI16 and 30 <= p <= 37 or 90 <= p <= 97:
            fg = ANSI16[p]
        elif p in ANSI16 and 40 <= p <= 47 or 100 <= p <= 107:
            bg = ANSI16[p]
        elif p == 38 and i + 1 < len(params):
            mode = params[i + 1]
            if mode == 5 and i + 2 < len(params):
                fg = xterm_256_to_hex(params[i + 2])
                i += 2
            elif mode == 2 and i + 4 < len(params):
                r, g, b = params[i + 2:i + 5]
                fg = f'#{r:02x}{g:02x}{b:02x}'
                i += 4
        elif p == 48 and i + 1 < len(params):
            mode = params[i + 1]
            if mode == 5 and i + 2 < len(params):
                bg = xterm_256_to_hex(params[i + 2])
                i += 2
            elif mode == 2 and i + 4 < len(params):
                r, g, b = params[i + 2:i + 5]
                bg = f'#{r:02x}{g:02x}{b:02x}'
                i += 4
        i += 1
    return fg, bg


def parse_ansi(text: str) -> list[list[Cell]]:
    text = text.replace('\r\n', '\n').replace('\r', '')
    lines: list[list[Cell]] = [[]]
    fg, bg = DEFAULT_FG, DEFAULT_BG
    idx = 0

    while idx < len(text):
        match = SGR_RE.match(text, idx)
        if match:
            raw = match.group(1)
            params = [int(p) for p in raw.split(';') if p] if raw else [0]
            fg, bg = apply_sgr(params, fg, bg)
            idx = match.end()
            continue

        ch = text[idx]
        idx += 1
        if ch == '\n':
            lines.append([])
            continue
        if ord(ch) < 32 and ch != '\t':
            continue
        lines[-1].append(Cell(ch, fg, bg))

    if lines and not lines[-1]:
        lines.pop()
    return lines or [[]]


def render_svg(lines: list[list[Cell]]) -> str:
    cols = max((len(line) for line in lines), default=0)
    rows = max(len(lines), 1)
    width = PAD_X * 2 + cols * CELL_W
    height = PAD_Y * 2 + rows * CELL_H

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
        f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" fill="{DEFAULT_BG}"/>',
        '<g font-family="Menlo, SFMono-Regular, ui-monospace, monospace" '
        f'font-size="{FONT_SIZE}" xml:space="preserve">',
    ]

    for row_idx, line in enumerate(lines):
        y = PAD_Y + row_idx * CELL_H
        for col_idx, cell in enumerate(line):
            x = PAD_X + col_idx * CELL_W
            if cell.bg != DEFAULT_BG:
                out.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL_W:.1f}" height="{CELL_H:.1f}" fill="{cell.bg}"/>'
                )
            if cell.char != ' ':
                out.append(
                    f'<text x="{x:.1f}" y="{y + FONT_SIZE:.1f}" fill="{cell.fg}">{html.escape(cell.char)}</text>'
                )

    out.append('</g>')
    out.append('</svg>')
    return '\n'.join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description='Render ANSI text to SVG.')
    parser.add_argument('input', help='Input .ansi or .txt file')
    parser.add_argument('output', help='Output .svg path')
    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    lines = parse_ansi(src.read_text())
    dst.write_text(render_svg(lines))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
