# Scenario format

Use a JSON object with optional top-level defaults and an ordered `steps` array.

## Top-level fields

- `width` — tmux pane width in columns
- `height` — tmux pane height in rows
- `cwd` — working directory override
- `steps` — ordered list of actions

## Step fields

A step may contain any combination of these fields:

- `note`: string, human-readable label only
- `wait`: number of seconds to sleep before the next action
- `send`: string or array of strings for named keys or short tokens
- `literal`: string to type literally with `tmux send-keys -l`
- `repeat`: integer; repeats `send` or `literal`
- `capture`: string label for the current screen dump

## Named keys

Supported aliases:

- `Enter`
- `Escape` / `Esc`
- `Up`
- `Down`
- `Left`
- `Right`
- `Space`
- `Tab`
- `Backspace`
- `Home`
- `End`
- `PageUp`
- `PageDown`
- `Delete`
- `C-c`
- `C-d`

Single-character values like `q`, `j`, `/`, `1` are sent literally.

## Example: simple boot + capture

```json
{
  "width": 110,
  "height": 32,
  "steps": [
    { "wait": 1.0, "capture": "01-start" },
    { "send": "q", "wait": 0.2, "capture": "02-after-q" }
  ]
}
```

## Example: Ockemon admin audit skeleton

```json
{
  "width": 110,
  "height": 34,
  "cwd": "/Users/gkk/DEV/ockemon-pso-omx",
  "steps": [
    { "wait": 1.2, "capture": "01-idle" },
    { "send": ["Right", "Right", "Enter"], "wait": 0.8, "capture": "02-open-panel" },
    { "send": "Enter", "wait": 0.8, "capture": "03-after-action" },
    { "send": "q", "wait": 0.2 }
  ]
}
```

Adjust the navigation keys to the actual TUI under test.

## Output structure

Each capture becomes files like:

- `01-idle.ansi`
- `01-idle.txt`
- `01-idle.svg`
- `01-idle.png`

A `manifest.json` file is also written to the output directory.
