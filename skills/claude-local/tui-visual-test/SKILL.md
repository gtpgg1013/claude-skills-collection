---
name: tui-visual-test
description: >
  ockemon-pso TUI 시각 테스트 — 렌더링 스냅샷, 인터랙션 플로우, 프레임 비교.
  ink-testing-library로 컴포넌트를 렌더링하고 lastFrame() 출력을 스냅샷으로 캡처.
  키 입력 시뮬레이션 → 프레임 전환 검증 → 레이아웃/색상/경계 확인.
  "visual test", "시각 테스트", "snapshot test", "프레임 테스트", "화면 테스트" 등으로 활성화.
argument-hint: "[component|panel|flow] [--update] [--interactive]"
---

<Purpose>
ockemon-pso TUI의 시각적 정확성을 검증하는 스킬.
기존 tui-test가 로직/상태 검증에 집중한다면, 이 스킬은:
1. 렌더링된 프레임(lastFrame)의 시각적 구조를 스냅샷으로 캡처/비교
2. 키 입력 시퀀스에 따른 화면 전환 플로우를 검증
3. 레이아웃(박스/테두리/정렬), 색상(ANSI), 텍스트 콘텐츠 검증
4. 회귀 감지 — 프레임 스냅샷이 변경되면 즉시 알림
</Purpose>

<Use_When>
- "visual test" / "시각 테스트" / "snapshot test" / "화면 테스트"
- "프레임 테스트" / "렌더링 테스트" / "레이아웃 테스트"
- 특정 대상: "visual test menu-bar", "visual test dex-panel"
- 플로우 테스트: "visual test navigation flow", "visual test feed flow"
- 스냅샷 갱신: "visual test --update" (기존 스냅샷 재캡처)
- 인터랙티브: "visual test --interactive" (tmux 실행 + 스크린샷)
</Use_When>

<Do_Not_Use_When>
- 로직/상태 유닛 테스트 → tui-test 스킬
- CLI 명령어 E2E 테스트 → e2e 테스트 직접 작성
- 웹 브라우저 테스트 → dogfood 스킬
- 빌드/타입 오류 → build-fix 스킬
</Do_Not_Use_When>

<Execution_Policy>
- 최대 5 사이클 (진단-수정 반복)
- 동일 실패 3회 연속 → 중단, 근본 원인 표시
- 파일 위치: packages/cli/src/tui/__tests__/visual/{target}.visual.test.tsx
- 스냅샷 위치: packages/cli/src/tui/__tests__/visual/__snapshots__/
- 기존 mock 패턴 준수 (references/mock-patterns.md in tui-test skill)
- ESM 호환: import .js 확장자, vi.hoisted() 필요 시
- afterEach에서 vi.restoreAllMocks()
</Execution_Policy>

<Steps>
## Phase 1: 대상 분석

1. **인수 파싱**: $ARGUMENTS에서 대상 결정
   - 컴포넌트명 → 해당 파일의 시각 테스트
   - `flow` → 인터랙션 플로우 테스트 (키 입력 시퀀스)
   - `--update` → 스냅샷 갱신 모드
   - `--interactive` → Phase 5 tmux 시각 테스트 포함

2. **소스 읽기**: 대상 컴포넌트의 렌더링 구조 분석
   ```
   Read packages/cli/src/tui/components/{target}.tsx
   Read packages/cli/src/tui/__tests__/{target}.test.tsx  (기존 테스트 있으면)
   ```

3. **시각 요소 식별**: 렌더링 출력에서 검증할 시각 요소 파악
   - Box 테두리 (borderStyle: round, single, double)
   - Text 색상 (color, dimColor, bold, inverse)
   - 레이아웃 (flexDirection, width, height, padding, margin)
   - 조건부 렌더링 (상태에 따른 표시/숨김)
   - 유니코드 문자 (█, ░, ╔, ═, ║, ✦, ✨ 등)

## Phase 2: 시각 테스트 설계

4. **테스트 유형 결정**:

   **A. 프레임 스냅샷 테스트** — 전체 렌더링 결과 비교
   ```typescript
   it('renders default state correctly', () => {
     const { lastFrame } = render(<Component {...props} />);
     expect(lastFrame()).toMatchSnapshot();
   });
   ```

   **B. 구조 검증 테스트** — 특정 시각 요소 존재 확인
   ```typescript
   it('shows border box with title', () => {
     const { lastFrame } = render(<Component />);
     const frame = lastFrame()!;
     expect(frame).toContain('╔');  // top border
     expect(frame).toContain('║');  // side border
     expect(frame).toContain('Title Text');
   });
   ```

   **C. 인터랙션 플로우 테스트** — 키 입력 → 프레임 변화
   ```typescript
   it('navigates right and highlights next item', async () => {
     const { lastFrame, stdin } = render(<MenuBar items={items} />);
     const before = lastFrame();

     stdin.write('\x1B[C');  // Right arrow
     await flush();

     const after = lastFrame();
     expect(before).not.toBe(after);  // 프레임 변경됨
     expect(after).toContain('Play');  // 새 항목 하이라이트
   });
   ```

   **D. 시각 회귀 테스트** — props 변경에 따른 프레임 변화
   ```typescript
   it('updates display when hunger changes', () => {
     const { lastFrame, rerender } = render(<StatusBars ockemon={ockemon} />);
     const before = lastFrame();

     rerender(<StatusBars ockemon={{...ockemon, damagotchi: {...ockemon.damagotchi, hunger: 20}}} />);
     const after = lastFrame();

     expect(before).not.toBe(after);
   });
   ```

5. **테스트 케이스 설계**:
   ```
   Task(subagent_type="oh-my-claudecode:test-engineer", model="sonnet", prompt="
     TARGET: {component name}
     TYPE: visual snapshot + interaction flow
     SOURCE: {file path and render structure}
     VISUAL ELEMENTS: {borders, colors, layout, unicode}
     OUTPUT: test case list with:
       - Snapshot tests (default state, edge states)
       - Structural tests (specific visual elements)
       - Interaction tests (key → frame transition)
       - Regression tests (prop changes → frame changes)
   ")
   ```

## Phase 3: 테스트 작성

6. **테스트 코드 작성**:
   ```
   Task(subagent_type="oh-my-claudecode:executor", model="sonnet", prompt="
     TASK: Write visual tests for {target}
     FILE: packages/cli/src/tui/__tests__/visual/{target}.visual.test.tsx
     TEMPLATE: templates/visual-test.md
     PATTERNS:
       - Snapshot: expect(lastFrame()).toMatchSnapshot()
       - Inline snapshot: expect(lastFrame()).toMatchInlineSnapshot()
       - Structure: expect(frame).toContain('╔')
       - Flow: stdin.write() → flush() → lastFrame() 비교
       - Rerender: rerender(<C newProps />) → lastFrame() 비교
       - Flush: await new Promise(r => setTimeout(r, 10))
     MOCK PATTERNS: tui-test/references/mock-patterns.md 참조
     KEYBOARD CODES: tui-test/references/keyboard-codes.md 참조
   ")
   ```

## Phase 4: 실행 + 수정 사이클 (max 5)

7. **테스트 실행**:
   ```bash
   pnpm --filter @ockemon/cli test src/tui/__tests__/visual/ 2>&1
   ```

8. **스냅샷 갱신** (--update 모드):
   ```bash
   pnpm --filter @ockemon/cli test src/tui/__tests__/visual/ -- --update 2>&1
   ```

9. **실패 시 진단 → 수정 → 재실행** (tui-test와 동일 사이클):
   ```
   [VISUAL-TEST Cycle {N}/5] Running {target} visual tests...
   [VISUAL-TEST Cycle {N}/5] {PASS|FAIL} — {details}
   ```

10. **전체 테스트 회귀 확인**:
    ```bash
    pnpm --filter @ockemon/cli test 2>&1
    ```

## Phase 5: --interactive 시각 테스트 (선택)

11. **tmux 기반 실제 화면 캡처**:
    ```
    Task(subagent_type="oh-my-claudecode:qa-tester", model="sonnet", prompt="
      VISUAL INSPECTION:
      Goal: Verify TUI renders correctly in real terminal
      Service: cd /Users/gkk/DEV/ockemon-pso && pnpm --filter @ockemon/cli build && node packages/cli/dist/index.js tui
      Capture:
        1. 초기 화면 — 메뉴바 + 스프라이트 + 상태바
        2. Right→Right→Enter — Train 패널 열림
        3. Esc — 메뉴 복귀
        4. Right x5 → Enter — Dex 패널 열림
        5. 'q' — 종료
      Verify: 레이아웃 깨짐 없음, 유니코드 정상, 색상 표시
    ")
    ```

## Phase 6: 검증

12. **증거 수집**:
    ```
    Task(subagent_type="oh-my-claudecode:verifier", model="sonnet", prompt="
      VERIFY: TUI visual test coverage
      EVIDENCE:
        1. Visual test file list
        2. Snapshot count
        3. All tests passing
        4. No regressions to existing tests
        5. Key visual elements covered (borders, colors, layout)
    ")
    ```
</Steps>

<Tool_Usage>
## 핵심 도구

| 도구 | 용도 |
|------|------|
| Read | 소스/테스트/스냅샷 파일 읽기 |
| Glob | 시각 테스트 파일 검색 |
| Grep | 렌더링 패턴/색상 코드 검색 |
| Write | 새 시각 테스트 파일 생성 |
| Edit | 기존 테스트 수정 |
| Bash | `pnpm test` 실행, `--update` 스냅샷 갱신 |
| Task | 에이전트 위임 |

## 에이전트 라우팅

| Phase | 에이전트 | 모델 | 역할 |
|-------|----------|------|------|
| 설계 | test-engineer | sonnet | 시각 테스트 케이스 목록 |
| 작성 | executor | sonnet | 시각 테스트 코드 구현 |
| 진단 | architect | opus | 스냅샷 불일치 근본 원인 |
| 수정 | executor | sonnet | 테스트 코드 수정 |
| E2E | qa-tester | sonnet | tmux 시각 검증 |
| 검증 | verifier | sonnet | 완료 증거 |
</Tool_Usage>

<Key_Concepts>
## 프레임 스냅샷 vs 구조 검증

**스냅샷** (`toMatchSnapshot`):
- 전체 렌더링 결과를 파일로 저장/비교
- 장점: 미세한 변화도 감지, 작성 쉬움
- 단점: 스타일 변경 시 대량 갱신 필요
- 용도: 안정된 컴포넌트의 회귀 감지

**인라인 스냅샷** (`toMatchInlineSnapshot`):
- 테스트 파일 내에 기대값 직접 포함
- 장점: 기대값이 테스트 코드에 바로 보임
- 단점: 긴 출력에는 부적합
- 용도: 짧은 출력, 핵심 프레임

**구조 검증** (`toContain`, `toMatch`):
- 특정 텍스트/패턴만 검증
- 장점: 스타일 변경에 강함, 의도가 명확
- 단점: 전체 레이아웃 깨져도 못 잡음
- 용도: 특정 요소 존재 확인

**권장**: 핵심 컴포넌트는 스냅샷 + 구조 검증 조합. 자주 변하는 컴포넌트는 구조 검증만.

## 프레임 디프 패턴

```typescript
function frameDiff(before: string, after: string): string[] {
  const bLines = before.split('\n');
  const aLines = after.split('\n');
  const diffs: string[] = [];
  const maxLen = Math.max(bLines.length, aLines.length);
  for (let i = 0; i < maxLen; i++) {
    if (bLines[i] !== aLines[i]) {
      diffs.push(`L${i + 1}: "${bLines[i] ?? ''}" → "${aLines[i] ?? ''}"`);
    }
  }
  return diffs;
}
```

## flush 유틸리티

```typescript
async function flush(ms = 10): Promise<void> {
  await new Promise(r => setTimeout(r, ms));
}
```
</Key_Concepts>

<Examples>
<Good>
/tui-visual-test menu-bar
→ MenuBar 렌더링 → 10개 항목 스냅샷 → 선택 하이라이트 검증 → narrow 모드 검증

/tui-visual-test dex-panel
→ DexPanel 렌더링 → FormCard 스냅샷 → 탭 전환 프레임 비교 → 하이브리드 그리드 레이아웃

/tui-visual-test navigation flow
→ App 렌더링 → Right→Right→Enter → 패널 열림 확인 → Esc → 메뉴 복귀 → 각 프레임 스냅샷

/tui-visual-test status-bars
→ StatusBars 렌더링 → hunger/mood/condition 바 스냅샷 → props 변경 → 바 길이 변화 검증

/tui-visual-test --update
→ 모든 시각 테스트 스냅샷 재캡처 (의도적 변경 후)
</Good>
<Bad>
/tui-visual-test (인수 없이) → "무엇을 시각 테스트할까요? (component|panel|flow)" 질문
/tui-visual-test use-menu → "use-menu는 훅입니다. 시각 테스트 대상이 아닙니다. /tui-test 사용" 안내
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- 동일 스냅샷 불일치 3회 연속 → 중단, "--update로 스냅샷 갱신 필요?" 확인
- 최대 5사이클 도달 → 남은 실패 목록과 함께 중단
- 빌드 오류 → "/build-fix 먼저 실행" 안내
- 타입 오류 → "tsc 해결 필요" 안내
- 프로덕션 코드 버그 발견 → 사용자에게 알리고 별도 수정 제안
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] 대상의 기본 상태(default props) 스냅샷 캡처됨
- [ ] 주요 상태 전환(active/inactive, empty/filled) 프레임 비교됨
- [ ] 키 입력 플로우 테스트됨 (해당 시)
- [ ] 기존 테스트 깨지지 않음 (전체 pnpm test 통과)
- [ ] 스냅샷 파일이 __snapshots__/ 에 정상 생성됨
- [ ] mock 패턴이 프로젝트 기존 패턴과 일관
- [ ] afterEach에서 vi.restoreAllMocks() 호출
- [ ] import 경로에 .js 확장자 포함 (ESM)
</Final_Checklist>

<Visual_Test_Priority>
HIGH ROI:
1. app.tsx — 전체 레이아웃, 메뉴+스프라이트+상태바 배치
2. menu-bar — 10항목 렌더링, 선택 하이라이트, narrow 모드
3. dex-panel — FormCard 그리드, 탭 전환, 하이브리드 레이아웃
4. status-bars — hunger/mood/condition 바 + XP 바

MEDIUM ROI:
5. feed-panel — 피딩 게임 진입/완료 화면
6. stats-panel — tendency radar + achievement grid
7. evolution-overlay — 세레모니 애니메이션 프레임
8. gacha-overlay — 4단계 연출 프레임

LOW ROI:
9. sprite-canvas — 스프라이트 렌더링 (이미 테스트됨)
10. ambient-layer — 파티클 렌더링 (랜덤성으로 스냅샷 부적합)
</Visual_Test_Priority>
