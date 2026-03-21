---
name: team-tui
description: "Full /team pipeline with parallel TUI test QA in the verify stage. Use when asked to 'team tui', 'team-tui', or when building/modifying TUI components that need automated testing after implementation."
---

# Team TUI

This skill extends `/team` with **parallel TUI testing QA** in the verify stage.
Instead of browser-based dogfood, it runs ink-testing-library + vitest unit tests
and optionally tmux-based interactive E2E tests on the ockemon-pso TUI.

## CRITICAL: Team Orchestration Requirement

**You MUST use the `/oh-my-claudecode:team` skill as the base orchestration mechanism.**

This means:
1. **FIRST**, invoke the `/team` skill via `Skill("oh-my-claudecode:team", args)` to set up proper Claude Code native team coordination
2. The `/team` skill handles: team creation, task decomposition, teammate spawning, stage transitions, and coordination
3. `/team-tui` ONLY adds the TUI test QA layer on top of `/team`'s verify stage
4. **Do NOT substitute Task agents for team coordination** — you must use `/team`'s native team mechanism

### How to Invoke

When `/team-tui` is triggered with arguments like `N "task description"`:

1. Parse the arguments to extract:
   - `N` — number of exec workers (optional, default from /team)
   - `task description` — the work to be done
   - `--tui-workers N` — number of TUI test workers in verify stage (default: 3)
   - `--interactive` — include tmux-based E2E tests alongside unit tests
   - `--fix` — focus on fixing existing failing TUI tests rather than writing new ones
   - `--scope component|hook|panel|all` — limit TUI test scope (default: auto from changed files)

2. Invoke the `/team` skill:
   ```
   Skill("oh-my-claudecode:team", "N \"task description\"")
   ```

3. The `/team` skill will run its standard pipeline:
   ```
   team-plan → team-prd → team-exec → team-verify → team-fix (loop)
   ```

4. **INTERCEPT at team-verify stage**: Before `/team` runs its standard verify, inject the TUI test QA workers alongside the standard verifiers.

### Interception Strategy

**Option A (Preferred): Invoke /team with modified instructions**

Pass the full context to `/team` so it knows to include TUI testing in its verify stage:

```
Skill("oh-my-claudecode:team", "N \"task description. IMPORTANT: During team-verify stage, in addition to standard verifier/reviewer agents, also spawn parallel TUI test workers. Each TUI test worker should: (1) identify changed/new TUI components from the exec stage, (2) write or update ink-testing-library + vitest tests for those components, (3) run 'pnpm --filter @ockemon/cli test' to verify all tests pass. Decompose TUI testing into N non-overlapping scopes: components, hooks, panels, integration. TUI test results determine pass/fail. Critical test failures (new tests fail, existing tests break) trigger team-fix loop.\"")
```

**Option B (If /team doesn't support inline verify customization):**

1. Run `/team` for `team-plan → team-prd → team-exec` stages
2. After team-exec completes, run your own verify stage that combines:
   - Standard verifier/reviewer agents (via Task tool)
   - Parallel TUI test workers (via Task tool)
3. If test failures found, create fix tasks and loop back

## Pipeline

```
team-plan → team-prd → team-exec → team-verify(+ parallel TUI QA) → team-fix (loop)
```

All stages are managed by the `/team` skill. The only addition is TUI test workers in the verify stage.

## Prerequisites Check (Before team-verify TUI QA)

Check prerequisites **once**, before the first verify stage that includes TUI testing.
This does NOT block team-plan, team-prd, or team-exec.

### Check 1: Test framework

```bash
pnpm --filter @ockemon/cli exec vitest --version
```

### Check 2: ink-testing-library

```bash
ls node_modules/ink-testing-library/package.json 2>/dev/null || \
ls packages/cli/node_modules/ink-testing-library/package.json 2>/dev/null
```

### Check 3: tui-test skill references

```bash
ls .claude/skills/tui-test/references/mock-patterns.md 2>/dev/null
```

If any prerequisite fails, fall back to standard `/team` verify (no TUI QA) and warn the user.

## How team-verify Changes

In standard `/team`, the verify stage runs:
- `verifier` (sonnet) — evidence-based completion check
- Optional: `security-reviewer`, `code-reviewer`, `quality-reviewer`

In `/team-tui`, the verify stage runs **all of the above PLUS**:

### Parallel TUI Test Workers

1. **Auto-detect changed TUI files** from the exec stage:

```bash
# Get files changed by exec workers
git diff --name-only HEAD~$(git log --oneline | head -5 | wc -l) -- packages/cli/src/tui/
```

From the changed files, categorize into test scopes:
- **components**: `packages/cli/src/tui/components/*.tsx`
- **hooks**: `packages/cli/src/tui/hooks/*.ts`
- **animation**: `packages/cli/src/tui/animation/*.ts`
- **integration**: `packages/cli/src/tui/app.tsx`, cross-cutting changes

2. **Spawn TUI test workers in parallel** alongside the standard verifier:

```
team-verify stage workers (managed by /team):
|- verifier (sonnet)           -- standard completion/code verification
|- code-reviewer (opus)        -- if >20 files changed
|- tui-test-worker-1           -- component tests (panels, overlays, presentational)
|- tui-test-worker-2           -- hook tests (use-menu, use-gacha, use-streak, etc.)
|- tui-test-worker-3           -- integration tests (app.tsx happy path, panel switching)
```

If `--interactive` flag:
```
|- tui-e2e-worker              -- tmux-based interactive TUI testing via qa-tester
```

3. **Each TUI test worker's task description MUST include:**

```
## Assignment

You are testing the ockemon-pso TUI: packages/cli/src/tui/
Your scope: {WORKER_SCOPE_AREA}
Output: test files at packages/cli/src/tui/__tests__/

## MANDATORY: Follow tui-test patterns

You MUST follow the project's established TUI test patterns.
Read these references before writing any test:

- Mock patterns: .claude/skills/tui-test/references/mock-patterns.md
- Keyboard codes: .claude/skills/tui-test/references/keyboard-codes.md
- Test gap checklist: .claude/skills/tui-test/references/test-gap-checklist.md

## Framework

- ink-testing-library v4: render(), lastFrame(), stdin.write(), stdout.frames
- vitest v3: describe/it/expect, vi.mock(), vi.useFakeTimers()
- strip-ansi: for snapshot comparison (if needed)

## Key Patterns

### DB Mock (every DB-touching component):
```typescript
vi.mock('../../db/connect.js', () => ({
  openDb: () => ({
    repoName: { method: vi.fn().mockReturnValue(data) },
    close: vi.fn(),
  }),
}));
```

### Keyboard Input:
```typescript
stdin.write('\r');        // Enter
stdin.write('\x1B');      // Escape
stdin.write('\x1B[C');    // Right arrow
await new Promise(r => setTimeout(r, 10)); // flush useEffect
```

### Animation:
```typescript
vi.useFakeTimers();
await vi.advanceTimersByTimeAsync(333); // 1 frame at 3 FPS
vi.useRealTimers();
```

## Scope Constraints

ONLY test the following area: {WORKER_SCOPE_AREA}
Changed files in your scope: {CHANGED_FILES_LIST}
Do NOT test outside your assigned scope.

## Success Criteria

1. All new tests pass: `pnpm --filter @ockemon/cli test {scope_pattern}`
2. No existing tests broken: `pnpm --filter @ockemon/cli test`
3. Each changed/new component has at least one test covering its primary behavior
4. import paths use .js extension (ESM)
5. afterEach calls vi.restoreAllMocks()
```

4. **E2E worker (--interactive mode) task description:**

```
## Assignment

You are performing interactive E2E testing of the ockemon TUI.
Use tmux to launch and interact with the actual TUI.

## Test Protocol (qa-tester 5-step)

1. PREREQUISITES: tmux installed, packages built
   ```bash
   pnpm --filter @ockemon/cli build
   ```

2. SETUP:
   ```bash
   tmux new-session -d -s tui-e2e-{timestamp} "node packages/cli/dist/index.js tui"
   ```

3. EXECUTE test cases:
   a. Menu renders with 10 items
      ```bash
      sleep 1 && tmux capture-pane -t tui-e2e-{ts} -p | grep -c "Feed\|Play\|Train\|Stats\|History\|Dex\|Challenge\|Storage\|Activity\|Settings"
      ```
   b. Right arrow navigation
      ```bash
      tmux send-keys -t tui-e2e-{ts} Right "" && sleep 0.3 && tmux capture-pane -t tui-e2e-{ts} -p
      ```
   c. Enter opens panel
      ```bash
      tmux send-keys -t tui-e2e-{ts} Enter "" && sleep 0.3 && tmux capture-pane -t tui-e2e-{ts} -p
      ```
   d. Esc returns to menu
      ```bash
      tmux send-keys -t tui-e2e-{ts} Escape "" && sleep 0.3 && tmux capture-pane -t tui-e2e-{ts} -p
      ```
   e. q exits
      ```bash
      tmux send-keys -t tui-e2e-{ts} q ""
      ```

4. VERIFY: check captured output against expected patterns → PASS/FAIL

5. CLEANUP:
   ```bash
   tmux kill-session -t tui-e2e-{ts}
   ```
```

## Verify Stage Outcome

The verify stage now produces TWO types of results:

### From standard verifier/reviewers:
- Code quality assessment
- Security review (if applicable)
- Completion evidence

### From TUI test workers:
- New/updated test files at `packages/cli/src/tui/__tests__/`
- Test execution results (pass/fail counts)
- E2E test evidence (tmux captures, if --interactive)

**Aggregation:** The lead collects results from all TUI test workers:
- Total tests: before vs after
- New tests added per scope
- All passing confirmation
- Any regressions found

### Pass/Fail Decision

The verify stage **fails** (→ team-fix) if:
- Standard verifier finds issues (same as `/team`), OR
- **Any existing TUI tests break** (regression — Critical severity), OR
- **New tests fail after 2 fix attempts within the worker** (High severity), OR
- **E2E tests detect broken navigation/rendering** (High severity)

The verify stage **passes** if:
- Standard verifier passes, AND
- All existing TUI tests still pass (no regressions), AND
- New tests pass or were successfully fixed by the worker, AND
- E2E tests pass (if --interactive)

Incomplete test coverage (gaps remain) is reported but does NOT block completion.

## team-fix Behavior

When verify fails due to TUI test findings:

### Regression fixes (Critical):
- Fix tasks reference the specific failing test file and error output
- Worker gets both the test source AND the production code to diagnose
- Uses architect (opus) for diagnosis, executor (sonnet) for fix
- Constraint: prefer fixing test code unless a real production bug is found

### New test failures (High):
- Worker reviews the test case design — was the test wrong or is there a real bug?
- If test is wrong: fix the test (mock pattern, async timing, assertion)
- If production bug: create separate fix task for the exec stage

### E2E failures:
- Capture tmux output as evidence
- Create targeted fix task with exact reproduction steps
- Re-run only the failing E2E scenario on re-verify

After fixes, the pipeline loops back: `team-exec → team-verify(+TUI QA)`
On re-verify, TUI workers re-run the full test suite plus re-check specific failures.

## Scope Auto-Detection

When `--scope` is not specified, auto-detect from exec stage changes:

```python
changed_files = git diff --name-only
tui_files = [f for f in changed_files if 'packages/cli/src/tui/' in f]

scopes = {
  'components': [f for f in tui_files if '/components/' in f],
  'hooks': [f for f in tui_files if '/hooks/' in f],
  'animation': [f for f in tui_files if '/animation/' in f],
  'integration': [f for f in tui_files if f.endswith('app.tsx') or f.endswith('index.tsx')],
}

# Only spawn workers for scopes with changed files
active_scopes = {k: v for k, v in scopes.items() if v}
```

If no TUI files changed, skip TUI QA entirely and use standard `/team` verify.

## Worker Scope Assignment

| Worker | Scope | Test Pattern | Files |
|--------|-------|-------------|-------|
| tui-test-worker-1 | components | `render()` + `lastFrame()` + `stdin.write()` | panels, overlays, presentational |
| tui-test-worker-2 | hooks | wrapper component + `lastFrame()` or `vi.useFakeTimers()` | use-menu, use-gacha, use-streak, etc. |
| tui-test-worker-3 | integration | full App render + mock all hooks + panel switching | app.tsx, cross-cutting |
| tui-e2e-worker | e2e (optional) | tmux + capture-pane | actual CLI binary |

## Everything Else

All other aspects are handled by the `/team` skill:
- **team-plan**: `explore` + `planner`, optionally `analyst`/`architect`
- **team-prd**: `analyst`, optionally `critic`
- **team-exec**: `executor` + task-appropriate specialists
- **team-fix**: `executor`/`build-fixer`/`debugger` depending on defect type
- **State persistence**: `state_write(mode="team")` with all standard fields
- **Handoff documents**: `.omc/handoffs/<stage-name>.md`
- **Shutdown protocol**: Standard team shutdown
- **Team + Ralph composition**: Supported (`/team-tui ralph "task"`)
- **Error handling**: Standard team error handling
- **Cancellation**: Standard `/oh-my-claudecode:cancel`

## Example

```
User: /team-tui 3 "add emotion system to TUI with animated expressions" --interactive

Step 1: Invoke /team skill
  Skill("oh-my-claudecode:team", "3 \"add emotion system to TUI with animated expressions\"")

Step 2: /team runs its pipeline
  team-plan:
    explore scans packages/cli/src/tui/, planner decomposes task

  team-prd:
    analyst defines: expression engine, bubble rendering, personality integration

  team-exec:
    worker-1: Implement expression engine (use-emotion.ts enhancements)
    worker-2: Implement animated bubble component (emotion-bubble.tsx)
    worker-3: Wire into app.tsx + sprite-canvas.tsx

Step 3: At team-verify, /team-tui adds TUI test workers
  team-verify:
    |- verifier: checks code quality, completion evidence
    |- tui-test-worker-1: component tests
    |    → writes emotion-bubble.test.tsx (render, expression types, animation)
    |    → writes sprite-canvas expression overlay tests
    |    → runs pnpm test → 2 new tests fail
    |    → self-fix: missing mock for useEmotion → fixes → ALL PASS
    |- tui-test-worker-2: hook tests
    |    → updates use-emotion.test.ts (new expression inputs)
    |    → writes use-pose expression integration test
    |    → runs pnpm test → ALL PASS
    |- tui-test-worker-3: integration tests
    |    → updates tui-app.test.tsx (emotion rendering in full app)
    |    → runs pnpm test → 1 FAIL (existing streak-bar test regression)
    |- tui-e2e-worker: tmux E2E
    |    → launches TUI, navigates to stats → confirms expression renders
    |    → PASS

  Results:
    verifier: PASS
    tui-tests: 1 regression (streak-bar.test.tsx broken by layout change)
    → FAIL (regression = Critical)

Step 4: /team runs team-fix
  team-fix:
    worker-1: Fix streak-bar.test.tsx regression
      → Layout moved streak bar position → update test assertion
      → pnpm test → ALL PASS

Step 5: Re-verify
  team-verify (round 2):
    |- verifier: PASS
    |- tui-test-workers: ALL PASS (143 tests, 12 new)
    |- tui-e2e-worker: PASS
    → PASS

complete:
  Total: 143 tests passing (+12 new)
  New coverage: emotion-bubble, use-emotion updates, app integration
  0 regressions remaining
```

## Comparison: team-tui vs team-dogfood

| Aspect | team-tui | team-dogfood |
|--------|----------|-------------|
| **Target** | Terminal UI (Ink/React) | Web UI (browser) |
| **Test tool** | ink-testing-library + vitest | agent-browser (Playwright) |
| **E2E tool** | tmux capture-pane | agent-browser screenshots/video |
| **Test output** | .test.tsx files + vitest results | report.md + screenshots + videos |
| **Evidence** | test pass/fail counts, code diffs | screenshots, recordings, repro steps |
| **Regression** | vitest detects automatically | manual visual comparison |
| **Severity model** | regression=Critical, new fail=High | Critical/High/Medium/Low taxonomy |
| **Artifacts** | test files (committed to repo) | dogfood-output/ reports (not committed) |
