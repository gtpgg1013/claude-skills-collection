# Mock Patterns — ockemon-pso TUI Tests

## 1. DB Mock (connect.js)

DB에 의존하는 컴포넌트/훅 테스트 시 사용.

```typescript
vi.mock('../../db/connect.js', () => ({
  openDb: () => ({
    ockemonRepo: {
      getActive: vi.fn().mockReturnValue({ id: 1, name: 'TestMon', xp: 500, hunger: 80, mood: 70 }),
      getAllOckemon: vi.fn().mockReturnValue([]),
      setActive: vi.fn(),
    },
    formRepo: {
      getCurrent: vi.fn().mockReturnValue({ id: 1, species: 'fire_basic', sprite_ansi: '🔥' }),
      getAll: vi.fn().mockReturnValue([]),
    },
    evolutionRepo: {
      getHistory: vi.fn().mockReturnValue([]),
    },
    activityRepo: {
      insert: vi.fn(),
      getDailyCount: vi.fn().mockReturnValue(0),
    },
    configRepo: {
      get: vi.fn().mockReturnValue(null),  // null = 기본값 (true for toggles)
      set: vi.fn(),
    },
    challengeRepo: {
      getTodayChallenges: vi.fn().mockReturnValue([]),
      updateProgress: vi.fn(),
    },
    questRepo: {
      getWeekQuests: vi.fn().mockReturnValue([]),
    },
    streakRepo: {
      getCurrent: vi.fn().mockReturnValue({ currentStreak: 5, longestStreak: 10 }),
      findRecent: vi.fn().mockReturnValue([]),
    },
    seasonRepo: {
      getCurrentProgress: vi.fn().mockReturnValue(null),
    },
    rewardRepo: {
      insert: vi.fn(),
    },
    close: vi.fn(),
  }),
}));
```

## 2. useOckemon Hook Mock

app.tsx나 패널 컴포넌트 테스트 시 — useOckemon을 통째로 mock.

```typescript
vi.mock('../hooks/use-ockemon.js', () => ({
  useOckemon: () => ({
    ockemon: {
      id: 1, name: 'TestMon', xp: 500, level: 5,
      hunger: 80, mood: 70, condition: 'normal',
      personality_type: 'brave', equipped_title: null,
      tendency_battle: 50, tendency_social: 30, tendency_knowledge: 60,
      tendency_creative: 40, tendency_nature: 20, tendency_chaos: 10,
    },
    form: {
      id: 1, species: 'fire_basic', display_name: 'Fire Basic',
      sprite_ansi: '🔥', rarity: 'common',
    },
    allForms: [],
    history: [],
    streakInfo: { currentStreak: 5, longestStreak: 10, todayActive: true },
    achievements: [],
    discoveredCount: 3,
    speciesDisplayName: 'Fire Basic',
    reload: vi.fn(),
  }),
}));
```

**주의**: tui-app.test.tsx 참고 — useOckemon 반환값의 **모든 필드**를 포함해야 함.

## 3. useMenu Hook Mock

패널 테스트에서 메뉴 상태가 필요할 때.

```typescript
vi.mock('../hooks/use-menu.js', () => ({
  useMenu: () => ({
    selectedIndex: 0,
    activePanel: null,
    select: vi.fn(),
    back: vi.fn(),
  }),
}));
```

## 4. useToast Mock

toast 발동을 확인할 때.

```typescript
const mockAddToast = vi.fn();
vi.mock('../hooks/use-toast.js', () => ({
  useToast: () => ({
    toasts: [],
    addToast: mockAddToast,
    dismissToast: vi.fn(),
  }),
}));
```

## 5. useTerminalSize Mock

특정 터미널 크기에서의 렌더링 테스트.

```typescript
vi.mock('../hooks/use-terminal-size.js', () => ({
  useTerminalSize: () => ({ columns: 80, rows: 24 }),
}));
```

## 6. Timer Mock (애니메이션)

```typescript
beforeEach(() => { vi.useFakeTimers(); });
afterEach(() => { vi.useRealTimers(); });

// 333ms = 1 animation frame (3 FPS)
await vi.advanceTimersByTimeAsync(333);

// 5초 = useOckemon refresh interval
await vi.advanceTimersByTimeAsync(5001);
```

## 7. ESM 호환 주의사항

watcher-recovery 테스트 패턴 참고 — `vi.hoisted()` 사용:

```typescript
const { mockFs } = vi.hoisted(() => ({
  mockFs: { readFileSync: vi.fn() },
}));
vi.mock('node:fs', () => mockFs);
```

## 8. Async useEffect Flush

```typescript
// useEffect 결과 대기
await new Promise(r => setTimeout(r, 10));

// 또는 act-like 패턴
await new Promise(resolve => setImmediate(resolve));
```
