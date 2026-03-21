#!/usr/bin/env python3
"""Run a terminal UI inside tmux, drive it with a JSON scenario, and capture screenshot artifacts."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ANSI_TO_SVG = SCRIPT_DIR / 'ansi_to_svg.py'

KEY_ALIASES = {
    'enter': 'Enter',
    'return': 'Enter',
    'esc': 'Escape',
    'escape': 'Escape',
    'up': 'Up',
    'down': 'Down',
    'left': 'Left',
    'right': 'Right',
    'space': 'Space',
    'tab': 'Tab',
    'backspace': 'BSpace',
    'home': 'Home',
    'end': 'End',
    'pageup': 'PageUp',
    'pagedown': 'PageDown',
    'delete': 'DC',
    'c-c': 'C-c',
    'c-d': 'C-d',
}


def sh(cmd: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(
        cmd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE if capture else subprocess.DEVNULL,
    )
    return result.stdout if capture else ''


def session_exists(name: str) -> bool:
    return subprocess.run(
        ['tmux', 'has-session', '-t', name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def normalize_label(label: str) -> str:
    cleaned = ''.join(ch.lower() if ch.isalnum() else '-' for ch in label.strip())
    while '--' in cleaned:
        cleaned = cleaned.replace('--', '-')
    return cleaned.strip('-') or 'capture'


def send_named_key(session: str, token: str) -> None:
    key = KEY_ALIASES.get(token.lower())
    target = f'{session}:0.0'
    if key is not None:
        sh(['tmux', 'send-keys', '-t', target, key])
    elif len(token) == 1:
        sh(['tmux', 'send-keys', '-t', target, '-l', token])
    else:
        sh(['tmux', 'send-keys', '-t', target, '-l', token])


def send_step(session: str, step: dict[str, Any]) -> None:
    repeat = int(step.get('repeat', 1))
    for _ in range(max(repeat, 1)):
        if 'literal' in step:
            sh(['tmux', 'send-keys', '-t', f'{session}:0.0', '-l', str(step['literal'])])
        if 'send' in step:
            payload = step['send']
            items = payload if isinstance(payload, list) else [payload]
            for item in items:
                send_named_key(session, str(item))


def render_png(svg_path: Path, png_path: Path) -> None:
    tmpdir = png_path.parent / '.qlmanage'
    if tmpdir.exists():
        shutil.rmtree(tmpdir)
    tmpdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ['qlmanage', '-t', '-s', '2000', '-o', str(tmpdir), str(svg_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    candidates = [tmpdir / f'{svg_path.name}.png', tmpdir / f'{svg_path.stem}.png']
    for candidate in candidates:
        if candidate.exists():
            if png_path.exists():
                png_path.unlink()
            candidate.replace(png_path)
            break
    shutil.rmtree(tmpdir, ignore_errors=True)


def capture(session: str, outdir: Path, index: int, label: str) -> dict[str, str]:
    safe = f'{index:02d}-{normalize_label(label)}'
    target = f'{session}:0.0'
    ansi = sh(['tmux', 'capture-pane', '-e', '-p', '-t', target], capture=True)
    text = sh(['tmux', 'capture-pane', '-p', '-t', target], capture=True)

    ansi_path = outdir / f'{safe}.ansi'
    txt_path = outdir / f'{safe}.txt'
    svg_path = outdir / f'{safe}.svg'
    png_path = outdir / f'{safe}.png'

    ansi_path.write_text(ansi)
    txt_path.write_text(text)
    subprocess.run([sys.executable, str(ANSI_TO_SVG), str(ansi_path), str(svg_path)], check=True)
    render_png(svg_path, png_path)

    return {
        'label': label,
        'ansi': ansi_path.name,
        'text': txt_path.name,
        'svg': svg_path.name,
        'png': png_path.name,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Drive a TUI in tmux and capture artifacts.')
    parser.add_argument('--command', required=True, help='Command to run inside tmux, e.g. "ockemon admin"')
    parser.add_argument('--scenario', required=True, help='Path to scenario JSON')
    parser.add_argument('--output-dir', required=True, help='Directory for capture artifacts')
    parser.add_argument('--cwd', help='Working directory override')
    parser.add_argument('--session-name', default='tui-visual-qa')
    parser.add_argument('--width', type=int, default=110)
    parser.add_argument('--height', type=int, default=34)
    parser.add_argument('--keep-session', action='store_true')
    args = parser.parse_args()

    scenario_path = Path(args.scenario)
    scenario = json.loads(scenario_path.read_text())
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    width = int(scenario.get('width', args.width))
    height = int(scenario.get('height', args.height))
    cwd = str(scenario.get('cwd', args.cwd or Path.cwd()))
    session = args.session_name

    if session_exists(session):
      sh(['tmux', 'kill-session', '-t', session])

    sh([
        'tmux', 'new-session', '-d', '-s', session,
        '-x', str(width), '-y', str(height),
        '-c', cwd,
        args.command,
    ])

    manifest: dict[str, Any] = {
        'command': args.command,
        'cwd': cwd,
        'width': width,
        'height': height,
        'scenario': str(scenario_path),
        'captures': [],
    }

    capture_index = 1
    try:
        for step in scenario.get('steps', []):
            if 'send' in step or 'literal' in step:
                send_step(session, step)
            if 'wait' in step:
                time.sleep(float(step['wait']))
            if 'capture' in step:
                manifest['captures'].append(capture(session, outdir, capture_index, str(step['capture'])))
                capture_index += 1
    finally:
        manifest_path = outdir / 'manifest.json'
        manifest_path.write_text(json.dumps(manifest, indent=2))
        if not args.keep_session and session_exists(session):
            sh(['tmux', 'kill-session', '-t', session])

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
