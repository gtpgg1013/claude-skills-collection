# Hook Test Template

```typescript
import { render } from 'ink-testing-library';
import React from 'react';
import { Text } from 'ink';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// === DB Mock (DB 의존 훅만) ===
vi.mock('../../db/connect.js', () => ({
  openDb: () => ({
    // 필요한 repo만 포함
    close: vi.fn(),
  }),
}));

// === Import (mock 선언 후) ===
import { useMyHook } from '../hooks/use-my-hook.js';

// === Test Helper Component ===
// 훅 결과를 텍스트로 렌더링하는 래퍼
const TestComponent = (props: Record<string, unknown>) => {
  const result = useMyHook(props);
  return <Text>{JSON.stringify(result)}</Text>;
};

// 특정 필드만 확인할 때
const FieldDisplay = (props: Record<string, unknown>) => {
  const { fieldA, fieldB } = useMyHook(props);
  return (
    <Text>
      {`A:${fieldA} B:${fieldB}`}
    </Text>
  );
};

describe('useMyHook', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  // --- 초기 상태 ---
  it('returns correct initial state', () => {
    const { lastFrame } = render(<TestComponent />);
    expect(lastFrame()).toContain('"expectedKey"');
  });

  // --- 파생 값 (pure useMemo 훅) ---
  it('computes derived value correctly', () => {
    const { lastFrame } = render(<FieldDisplay input={42} />);
    expect(lastFrame()).toContain('A:expected');
  });

  // --- Props 변경에 반응 ---
  it('updates when inputs change', () => {
    const { lastFrame, rerender } = render(<FieldDisplay input={1} />);
    expect(lastFrame()).toContain('A:result1');
    rerender(<FieldDisplay input={2} />);
    expect(lastFrame()).toContain('A:result2');
  });

  // --- 타이머 기반 (폴링 훅) ---
  it('refreshes on interval', async () => {
    vi.useFakeTimers();
    const { lastFrame } = render(<TestComponent />);

    const initial = lastFrame();
    await vi.advanceTimersByTimeAsync(5001); // 5s refresh
    const updated = lastFrame();

    // DB mock 리턴값을 바꿔서 비교하거나, 호출 횟수 확인
    expect(updated).toBeDefined();

    vi.useRealTimers();
  });

  // --- 사이드이펙트 (toast 발동 등) ---
  it('triggers side effect on state change', async () => {
    const mockCallback = vi.fn();

    // 사이드이펙트를 감지할 수 있는 래퍼
    const SideEffectTest = () => {
      const result = useMyHook({ onChange: mockCallback });
      return <Text>{String(result)}</Text>;
    };

    const { rerender } = render(<SideEffectTest />);
    // 첫 렌더 — 사이드이펙트 없음
    expect(mockCallback).not.toHaveBeenCalled();

    // 데이터 변경 시뮬레이션 (rerender or timer advance)
    rerender(<SideEffectTest />);
    await new Promise(r => setTimeout(r, 10));
    // expect(mockCallback).toHaveBeenCalledWith(expectedArg);
  });

  // --- 키보드 입력 (useInput 기반 훅) ---
  it('handles keyboard input', async () => {
    const InputTest = () => {
      const { selectedIndex } = useMyHook();
      return <Text>{`selected:${selectedIndex}`}</Text>;
    };

    const { stdin, lastFrame } = render(<InputTest />);
    expect(lastFrame()).toContain('selected:0');

    stdin.write('\x1B[C'); // Right arrow
    await new Promise(r => setTimeout(r, 10));
    expect(lastFrame()).toContain('selected:1');
  });

  // --- 엣지 케이스 ---
  it('handles null/undefined input', () => {
    const { lastFrame } = render(<TestComponent input={null} />);
    expect(lastFrame()).not.toContain('undefined');
    expect(lastFrame()).not.toContain('NaN');
  });

  // --- 클린업 ---
  it('cleans up on unmount', () => {
    vi.useFakeTimers();
    const { unmount } = render(<TestComponent />);
    unmount();
    // interval이 정리되었는지 확인
    expect(() => vi.advanceTimersByTimeAsync(10000)).not.toThrow();
    vi.useRealTimers();
  });
});
```

## Pure Hook vs DB Hook 판별

| 훅 타입 | 특성 | mock 필요 |
|---------|------|----------|
| Pure (useMemo) | use-emotion, use-pose | 없음 — props만 전달 |
| Timer (useInterval) | use-ockemon, use-personality | vi.useFakeTimers() + DB mock |
| Event (useInput) | use-menu | stdin.write() |
| Side-effect | use-streak, use-achievements | 콜백 mock + rerender |
| DB one-shot | use-challenges, use-season | DB mock |

## Checklist

- [ ] `afterEach`에서 `vi.restoreAllMocks()` + `vi.useRealTimers()` (fake timers 사용 시)
- [ ] import 경로에 `.js` 확장자 포함
- [ ] 훅을 직접 호출하지 않고 래퍼 컴포넌트로 렌더링
- [ ] pure hook은 입력 순열 테스트 (경계값 포함)
- [ ] timer hook은 advance 후 결과 확인
- [ ] useInput hook은 stdin.write() + flush
