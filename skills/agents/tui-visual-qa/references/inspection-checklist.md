# TUI inspection checklist

## Visual integrity

- Is the main character/sprite centered correctly?
- Is any part cropped or clipped?
- Do equipment pieces sit on the correct body region?
- Is there accidental overlap, floating gear, or z-order inversion?
- Do borders, menus, and panels align cleanly?
- Does the terminal-size guard still work?

## State comparisons

- Compare base vs equipped
- Compare before vs after level-up/evolution
- Compare adjacent animation states when drift is suspected
- Compare the same screen at two terminal sizes if layout is responsive

## Interaction integrity

- Does focus move predictably with arrows/tab?
- Does Enter trigger the expected action?
- Does Escape/back return correctly?
- Are transient states visible long enough to inspect?

## Report format

For each issue, capture:
- `frame`: artifact filename
- `severity`: visual nit / functional bug / blocking bug
- `repro`: exact key path
- `expected`
- `actual`
- `notes`: alignment, clipping, design inconsistency, etc.
