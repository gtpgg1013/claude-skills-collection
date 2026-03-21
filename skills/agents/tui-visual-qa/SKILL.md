---
name: tui-visual-qa
description: Script, drive, and visually inspect terminal UIs/TUIs with deterministic tmux sessions, keyboard scenarios, pane captures, and PNG/SVG screenshot artifacts. Use when Codex needs to QA a CLI/TUI like ockemon admin, compare character or equipment states across level-ups, capture screenshots for design review, reproduce keyboard-navigation bugs, or audit layout/design regressions in a terminal app.
---

# TUI Visual QA

Use this skill to test a terminal UI like a human would: launch it in a fixed-size terminal, send keys through a scripted scenario, capture the screen at important states, and review image artifacts instead of guessing from logs.

## Quick start

1. Ground the target command and working directory.
2. Create a scenario JSON; see `references/scenario-format.md`.
3. Run:
   - `scripts/run_tui_scenario.py --command 'ockemon admin' --cwd /path/to/repo --scenario /tmp/admin-flow.json --output-dir /tmp/ockemon-admin-artifacts`
4. Review the generated `.png` files first. Open them with the local image tool when available.
5. Report findings with the exact frame file, scenario step, key sequence, and reproduction path.

## When to prefer this skill

Use this skill when the user wants any of the following in a terminal UI:
- visual QA
- screenshot-based review
- step-by-step interaction testing
- design inspection across multiple states
- equipment/character/evolution comparisons
- keyboard navigation bug reproduction
- artifact capture for handoff

## Workflow

### 1. Lock the environment

- Use a fixed terminal size for comparable captures.
- Prefer deterministic state setup before driving the TUI.
- For game/admin flows, use debug/admin commands to force states instead of waiting for organic progression.
- Keep command, cwd, width, and height identical across “before/after” comparisons.

### 2. Write a scenario

Model the interaction as ordered steps.
Supported step fields are intentionally small:
- `note`
- `wait`
- `send`
- `literal`
- `repeat`
- `capture`

See `references/scenario-format.md` for the schema and examples.

### 3. Capture proof artifacts

`run_tui_scenario.py` produces, per capture:
- `.ansi` — raw escape-sequence pane dump
- `.txt` — plain-text pane dump
- `.svg` — rendered terminal image
- `.png` — Quick Look thumbnail from the SVG
- `manifest.json` — scenario metadata + artifact index

The PNGs are the fastest way to inspect layout, clipping, overlap, and visual drift.

### 4. Inspect like a human reviewer

Use `references/inspection-checklist.md` as the default rubric.
Focus on:
- silhouette and proportion changes by level/form
- equipment anchor correctness
- overlap/clipping/z-order issues
- animation drift between adjacent captures
- menu focus and keyboard flow
- text wrapping, truncation, and empty-state layout
- narrow-terminal regressions

### 5. Report with evidence

For each issue, include:
- frame filename
- command + cwd
- exact scenario step / key sequence
- expected vs actual
- whether the bug is visual-only or functionally blocking

## Ockemon-specific guidance

For `ockemon admin`-style checks, capture at minimum:
- base idle state
- admin panel open
- post-equip state
- post-evolution state
- at least one additional animation/frame-adjacent state if alignment drift is suspected

If comparing multiple characters or growth stages, keep them in separate output folders but reuse the same terminal dimensions.

## Resources

- `scripts/run_tui_scenario.py` — launch + drive a TUI in tmux and capture artifacts
- `scripts/ansi_to_svg.py` — render captured terminal output into SVG
- `references/scenario-format.md` — step format and examples
- `references/inspection-checklist.md` — QA rubric for visual/debug review
