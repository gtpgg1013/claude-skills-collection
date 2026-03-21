# Visual Test Template

## Component Visual Test

```typescript
import React from 'react';
import { render } from 'ink-testing-library';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// --- Mocks (프로젝트 패턴 참조: tui-test/references/mock-patterns.md) ---

vi.mock('../../db/connect.js', () => ({
  openDb: () => ({
    // 필요한 repo mock 추가
    close: vi.fn(),
  }),
}));

// --- Import (mock 선언 이후!) ---
import { TargetComponent } from '../components/target-component.js';

// --- Helpers ---
async function flush(ms = 10): Promise<void> {
  await new Promise(r => setTimeout(r, ms));
}

describe('TargetComponent visual', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  // === A. 프레임 스냅샷 ===
  it('renders default state', () => {
    const { lastFrame } = render(<TargetComponent />);
    expect(lastFrame()).toMatchSnapshot();
  });

  it('renders empty state', () => {
    const { lastFrame } = render(<TargetComponent data={null} />);
    expect(lastFrame()).toMatchSnapshot();
  });

  // === B. 구조 검증 ===
  it('shows border box', () => {
    const { lastFrame } = render(<TargetComponent />);
    const frame = lastFrame()!;
    expect(frame).toContain('╔');
    expect(frame).toContain('║');
    expect(frame).toContain('╚');
  });

  it('displays title text', () => {
    const { lastFrame } = render(<TargetComponent title="My Title" />);
    expect(lastFrame()).toContain('My Title');
  });

  it('shows unicode progress bar', () => {
    const { lastFrame } = render(<TargetComponent value={50} max={100} />);
    const frame = lastFrame()!;
    expect(frame).toContain('█');
    expect(frame).toContain('░');
  });

  // === C. 인터랙션 플로우 ===
  it('changes highlight on right arrow', async () => {
    const { lastFrame, stdin } = render(<TargetComponent />);
    const before = lastFrame();

    stdin.write('\x1B[C'); // Right arrow
    await flush();

    const after = lastFrame();
    expect(before).not.toBe(after);
  });

  it('opens panel on Enter', async () => {
    const { lastFrame, stdin } = render(<TargetComponent />);

    stdin.write('\r'); // Enter
    await flush();

    expect(lastFrame()).toContain('Panel Content');
  });

  it('returns to menu on Escape', async () => {
    const { lastFrame, stdin } = render(<TargetComponent />);

    stdin.write('\r'); // Enter → open panel
    await flush();

    stdin.write('\x1B'); // Escape → close panel
    await flush();

    expect(lastFrame()).toContain('Menu');
  });

  // === D. 시각 회귀 ===
  it('updates bar when value changes', () => {
    const { lastFrame, rerender } = render(<TargetComponent value={80} />);
    const before = lastFrame();

    rerender(<TargetComponent value={20} />);
    const after = lastFrame();

    expect(before).not.toBe(after);
  });
});
```

## Flow (Multi-Step Interaction) Test

```typescript
import React from 'react';
import { render } from 'ink-testing-library';
import { describe, it, expect, vi, afterEach } from 'vitest';

// ... mocks ...

import { App } from '../app.js';

async function flush(ms = 10): Promise<void> {
  await new Promise(r => setTimeout(r, ms));
}

describe('Navigation flow visual', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('full menu navigation cycle', async () => {
    const { lastFrame, stdin } = render(<App />);
    const frames: string[] = [];

    // Frame 0: 초기 화면
    frames.push(lastFrame()!);
    expect(frames[0]).toContain('Feed'); // 첫 메뉴 항목

    // Frame 1: Right → Play 하이라이트
    stdin.write('\x1B[C');
    await flush();
    frames.push(lastFrame()!);

    // Frame 2: Right → Train 하이라이트
    stdin.write('\x1B[C');
    await flush();
    frames.push(lastFrame()!);

    // Frame 3: Enter → 패널 열림
    stdin.write('\r');
    await flush();
    frames.push(lastFrame()!);

    // Frame 4: Escape → 메뉴 복귀
    stdin.write('\x1B');
    await flush();
    frames.push(lastFrame()!);

    // 프레임 변화 검증
    expect(frames[0]).not.toBe(frames[1]); // Right 이동
    expect(frames[2]).not.toBe(frames[3]); // 패널 열림
    expect(frames[4]).not.toContain('Panel'); // 메뉴 복귀

    // 스냅샷 (선택적)
    expect(frames[0]).toMatchSnapshot('initial');
    expect(frames[3]).toMatchSnapshot('panel-open');
  });
});
```

## Snapshot Update

스냅샷을 의도적으로 변경했을 때:

```bash
# 특정 테스트 스냅샷 갱신
pnpm --filter @ockemon/cli test src/tui/__tests__/visual/{target}.visual.test.tsx -- --update

# 전체 시각 테스트 스냅샷 갱신
pnpm --filter @ockemon/cli test src/tui/__tests__/visual/ -- --update
```
