# Visual Test Patterns — ockemon-pso TUI

## 1. 프레임 캡처 기본

```typescript
import { render } from 'ink-testing-library';

const { lastFrame, stdin, rerender } = render(<Component />);

// lastFrame() → 현재 렌더링된 터미널 출력 (string | undefined)
// stdin.write(key) → 키 입력 시뮬레이션
// rerender(<Component newProps />) → props 변경 후 재렌더링
```

## 2. 스냅샷 전략

### 파일 스냅샷 (안정 컴포넌트)
```typescript
expect(lastFrame()).toMatchSnapshot();
// → __snapshots__/{file}.visual.test.tsx.snap 에 저장
```

### 인라인 스냅샷 (짧은 출력)
```typescript
expect(lastFrame()).toMatchInlineSnapshot(`
  "╔══════╗
   ║ Test ║
   ╚══════╝"
`);
```

### 구조 단언 (자주 변하는 컴포넌트)
```typescript
const frame = lastFrame()!;
expect(frame).toContain('Expected Text');
expect(frame).not.toContain('Should Not Appear');
expect(frame.split('\n').length).toBeGreaterThan(5);
```

## 3. 프레임 비교 패턴

### 변경 감지
```typescript
const before = lastFrame();
// ... action ...
const after = lastFrame();
expect(before).not.toBe(after); // 프레임이 변경됨
```

### 특정 라인 변경
```typescript
const beforeLines = lastFrame()!.split('\n');
stdin.write('\x1B[C');
await flush();
const afterLines = lastFrame()!.split('\n');

// 메뉴 라인(첫번째 줄)만 변경되었는지
expect(beforeLines[0]).not.toBe(afterLines[0]);
// 나머지는 유지
expect(beforeLines.slice(1)).toEqual(afterLines.slice(1));
```

## 4. ANSI 색상 검증

ink-testing-library의 lastFrame()은 ANSI 이스케이프 코드를 포함합니다.

```typescript
// 색상이 적용되었는지 (ANSI escape 존재)
expect(lastFrame()).toMatch(/\x1B\[/);

// 특정 텍스트에 bold 적용
expect(lastFrame()).toMatch(/\x1B\[1m.*Title.*\x1B\[22m/);
```

## 5. 레이아웃 검증

### 박스 테두리 (Ink Box)
```typescript
const frame = lastFrame()!;
// round border
expect(frame).toContain('╭');
expect(frame).toContain('╮');
expect(frame).toContain('╰');
expect(frame).toContain('╯');

// single border
expect(frame).toContain('┌');
expect(frame).toContain('┐');
expect(frame).toContain('└');
expect(frame).toContain('┘');

// double border (status command style)
expect(frame).toContain('╔');
expect(frame).toContain('╗');
expect(frame).toContain('╚');
expect(frame).toContain('╝');
```

### 프레임 높이/너비
```typescript
const lines = lastFrame()!.split('\n');
expect(lines.length).toBe(expectedHeight);
expect(lines[0]!.length).toBeLessThanOrEqual(maxWidth);
```

## 6. 유니코드 문자 검증

```typescript
// 프로그레스 바
expect(frame).toContain('█');  // 채워진 부분
expect(frame).toContain('░');  // 빈 부분

// Rarity/shiny 마커
expect(frame).toContain('✦');  // shiny sparkle
expect(frame).toContain('✨'); // hatching sparkle

// 하이브리드 디스커버리
expect(frame).toContain('●');  // discovered
expect(frame).toContain('○');  // undiscovered

// 스프라이트 문자
expect(frame).toContain('▀');  // half-block upper
expect(frame).toContain('▄');  // half-block lower
```

## 7. 조건부 렌더링

```typescript
// 빈 상태
const { lastFrame } = render(<List items={[]} />);
expect(lastFrame()).toContain('No items');

// 데이터 있는 상태
const { lastFrame: frame2 } = render(<List items={['a','b']} />);
expect(frame2()).not.toContain('No items');
expect(frame2()).toContain('a');
```

## 8. 애니메이션 프레임 캡처

```typescript
beforeEach(() => { vi.useFakeTimers(); });
afterEach(() => { vi.useRealTimers(); });

it('animates through frames', async () => {
  const { lastFrame } = render(<AnimatedComponent />);
  const frame0 = lastFrame();

  await vi.advanceTimersByTimeAsync(333); // 1 frame at 3 FPS
  const frame1 = lastFrame();

  await vi.advanceTimersByTimeAsync(333);
  const frame2 = lastFrame();

  // 프레임이 변화했는지
  expect(frame0).not.toBe(frame1);
});
```

## 9. 터미널 크기 의존 렌더링

```typescript
vi.mock('../hooks/use-terminal-size.js', () => ({
  useTerminalSize: () => ({ columns: 80, rows: 24 }),
}));

it('hides instructions in narrow terminal', () => {
  // columns < 70이면 숨김
  vi.mocked(useTerminalSize).mockReturnValue({ columns: 60, rows: 24 });
  const { lastFrame } = render(<MenuBar items={items} />);
  expect(lastFrame()).not.toContain('←/→ navigate');
});
```

## 10. 멀티프레임 시퀀스 헬퍼

```typescript
async function captureFrames(
  render: ReturnType<typeof render>,
  actions: Array<() => void | Promise<void>>,
): Promise<string[]> {
  const frames: string[] = [render.lastFrame()!];
  for (const action of actions) {
    await action();
    await flush();
    frames.push(render.lastFrame()!);
  }
  return frames;
}

// Usage:
const result = render(<App />);
const frames = await captureFrames(result, [
  () => result.stdin.write('\x1B[C'),  // Right
  () => result.stdin.write('\x1B[C'),  // Right
  () => result.stdin.write('\r'),       // Enter
  () => result.stdin.write('\x1B'),     // Escape
]);

expect(frames).toHaveLength(5);
expect(frames[0]).not.toBe(frames[1]); // 첫 이동
expect(frames[3]).not.toBe(frames[4]); // 패널 닫힘
```
