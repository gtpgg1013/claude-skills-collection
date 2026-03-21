# Component Test Template

```typescript
import { render } from 'ink-testing-library';
import React from 'react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// === DB Mock (DB 의존 컴포넌트만) ===
vi.mock('../../db/connect.js', () => ({
  openDb: () => ({
    // 필요한 repo만 포함
    ockemonRepo: { getActive: vi.fn().mockReturnValue(null) },
    configRepo: { get: vi.fn().mockReturnValue(null), set: vi.fn() },
    close: vi.fn(),
  }),
}));

// === Hook Mock (외부 훅 의존 시) ===
// vi.mock('../hooks/use-ockemon.js', () => ({
//   useOckemon: () => ({ ockemon: mockOckemon, form: mockForm, ... }),
// }));

// === Import (mock 선언 후) ===
import { ComponentName } from '../components/component-name.js';

// === Test Data ===
const defaultProps = {
  // 컴포넌트 props
};

describe('ComponentName', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  // --- 초기 렌더 ---
  it('renders initial state correctly', () => {
    const { lastFrame } = render(<ComponentName {...defaultProps} />);
    expect(lastFrame()).toContain('expected text');
  });

  // --- Props 변경 ---
  it('updates when props change', () => {
    const { lastFrame, rerender } = render(<ComponentName count={0} />);
    expect(lastFrame()).toContain('0');
    rerender(<ComponentName count={1} />);
    expect(lastFrame()).toContain('1');
  });

  // --- 키보드 입력 ---
  it('responds to keyboard input', async () => {
    const onAction = vi.fn();
    const { stdin, lastFrame } = render(
      <ComponentName onAction={onAction} />
    );
    stdin.write('\r'); // Enter
    await new Promise(r => setTimeout(r, 10));
    expect(onAction).toHaveBeenCalled();
    expect(lastFrame()).toContain('after action');
  });

  // --- 콜백 ---
  it('calls callback on completion', async () => {
    const onComplete = vi.fn();
    const { stdin } = render(<ComponentName onComplete={onComplete} />);
    stdin.write('\r');
    await new Promise(r => setTimeout(r, 10));
    expect(onComplete).toHaveBeenCalledWith(expect.objectContaining({
      // expected result shape
    }));
  });

  // --- 빈 상태 ---
  it('handles empty/null data gracefully', () => {
    const { lastFrame } = render(<ComponentName data={null} />);
    expect(lastFrame()).not.toContain('undefined');
  });

  // --- 스냅샷 ---
  it('matches snapshot', () => {
    const { lastFrame } = render(<ComponentName {...defaultProps} />);
    expect(lastFrame()).toMatchSnapshot();
  });
});
```

## Checklist

- [ ] `afterEach`에서 `vi.restoreAllMocks()` 호출
- [ ] import 경로에 `.js` 확장자 포함
- [ ] DB mock은 필요한 repo만 포함
- [ ] 비동기 작업 후 `await new Promise(r => setTimeout(r, 10))`
- [ ] React.memo 컴포넌트는 `rerender`로 props 변경 테스트
