---
name: tui-test
description: >
  ockemon-pso TUI 컴포넌트/훅/패널 테스트 작성 및 실행.
  ink-testing-library + vitest로 테스트를 작성하고, 실패 시 진단-수정 사이클을 반복.
  "tui test", "TUI 테스트", "tui coverage", "test feed-panel", "test use-menu" 등으로 활성화.
argument-hint: "[component|hook|panel|all] [--fix] [--interactive]"
---

<Purpose>
ockemon-pso TUI의 테스트 갭을 분석하고, ink-testing-library + vitest로
테스트를 작성하며, 실패 시 architect 진단 → executor 수정 사이클을 반복하는 스킬.
packages/cli/src/tui/ 내 27개 컴포넌트, 16개 훅, 4개 애니메이션 모듈 대상.
</Purpose>

<Use_When>
- "tui test" / "TUI 테스트" / "tui coverage"
- 특정 대상 테스트: "test feed-panel", "test use-menu", "test gacha-overlay"
- 전체 TUI 테스트: "tui test all"
- 인터랙티브 E2E: "tui test --interactive"
- 테스트 갭 분석만: "tui test --analyze"
</Use_When>

<Do_Not_Use_When>
- 웹 브라우저 테스트 → dogfood 스킬
- core/plugin 패키지 유닛 테스트 → 일반 test 명령
- 빌드 오류 수정 → build-fix 스킬
- 타입 에러 수정 → tsc 먼저
</Do_Not_Use_When>

<Execution_Policy>
- 최대 5 사이클 (ultraqa 패턴)
- 동일 실패 3회 연속 → 중단, 근본 원인 표시
- 새 테스트: packages/cli/src/tui/__tests__/{target}.test.tsx
- 기존 mock 패턴 준수 (vi.mock connect.js)
- React.memo 컴포넌트: rerender로 props 변경 테스트
- 애니메이션: vi.useFakeTimers() + vi.advanceTimersByTimeAsync()
- stdin 입력: stdin.write() (키 코드표는 references/keyboard-codes.md 참조)
</Execution_Policy>

<Steps>
## Phase 1: 대상 분석

1. **인수 파싱**: $ARGUMENTS에서 대상 결정
   - 컴포넌트명 → 해당 파일만
   - `all` → 전체 갭 우선순위 순서로
   - `--analyze` → 분석만 하고 종료
   - `--fix` → 기존 실패 테스트 수정에 집중
   - `--interactive` → Phase 4의 tmux E2E 포함

2. **소스 분석**: 대상 파일 읽기
   ```
   Read packages/cli/src/tui/components/{target}.tsx
   Read packages/cli/src/tui/hooks/{target}.ts
   ```

3. **기존 테스트 확인**:
   ```
   Glob packages/cli/src/tui/__tests__/{target}*.test.{ts,tsx}
   ```

4. **갭 식별**: 테스트되지 않은 경로, 분기, 상호작용 파악
   - references/test-gap-checklist.md 참조

## Phase 2: 테스트 설계 + 작성

5. **테스트 케이스 설계**:
   ```
   Task(subagent_type="oh-my-claudecode:test-engineer", model="sonnet", prompt="
     TARGET: {component/hook name}
     SOURCE: {file path and key logic}
     EXISTING TESTS: {existing test file or 'none'}
     MOCK PATTERN: references/mock-patterns.md 참조
     FRAMEWORK: ink-testing-library v4 + vitest v3
     OUTPUT: numbered test case list with:
       - describe/it 구조
       - 각 케이스의 setup, action, assertion
       - 필요한 mock 목록
   ")
   ```

6. **테스트 코드 작성**:
   ```
   Task(subagent_type="oh-my-claudecode:executor", model="sonnet", prompt="
     TASK: Write tests for {target}
     TEST CASES: {from step 5}
     FILE: packages/cli/src/tui/__tests__/{target}.test.tsx
     TEMPLATE: templates/component-test.md 또는 templates/hook-test.md
     PATTERNS:
       - DB mock: vi.mock('../../db/connect.js', ...)
       - Hook mock: vi.mock('../hooks/use-ockemon.js', ...)
       - Keyboard: stdin.write('\r') for Enter, '\x1B[C' for Right
       - Async: await new Promise(r => setTimeout(r, 10))
       - Animation: vi.useFakeTimers() + vi.advanceTimersByTimeAsync(333)
     CONSTRAINTS:
       - ESM 호환 (vi.hoisted 사용 필요 시)
       - import 경로 .js 확장자 포함
       - afterEach에서 vi.restoreAllMocks()
   ")
   ```

## Phase 3: 실행 + 수정 사이클 (max 5)

7. **테스트 실행**:
   ```bash
   pnpm --filter @ockemon/cli test {target} 2>&1
   ```

8. **결과 판정**:
   - ALL PASS → Phase 4로
   - FAIL → 계속

9. **실패 진단**:
   ```
   Task(subagent_type="oh-my-claudecode:architect", model="opus", prompt="
     FAILING TEST: {test name and file}
     ERROR OUTPUT: {vitest error}
     SOURCE CODE: {component/hook source}
     TEST CODE: {test source}
     TASK: Diagnose root cause. Output:
       1. Root cause (1 sentence)
       2. Fix location (file:line)
       3. Exact fix (code diff)
   ")
   ```

10. **수정 적용**:
    ```
    Task(subagent_type="oh-my-claudecode:executor", model="sonnet", prompt="
      APPLY FIX: {from architect diagnosis}
      FILE: {test file path}
      CONSTRAINT: Only modify test code, never production code
        (unless the test reveals an actual bug)
    ")
    ```

11. **사이클 반복**: → Step 7로

    진행 보고:
    ```
    [TUI-TEST Cycle {N}/5] Running {target} tests...
    [TUI-TEST Cycle {N}/5] {PASS|FAIL} — {details}
    ```

## Phase 4: 검증

12. **전체 테스트 실행**:
    ```bash
    pnpm --filter @ockemon/cli test 2>&1
    ```
    기존 테스트가 깨지지 않았는지 확인.

13. **증거 수집** (all 모드):
    ```
    Task(subagent_type="oh-my-claudecode:verifier", model="sonnet", prompt="
      VERIFY: TUI test coverage improvement
      EVIDENCE NEEDED:
        1. New test file list
        2. Test count before vs after
        3. All tests passing confirmation
        4. Coverage of identified gaps
    ")
    ```

## Phase 5: --interactive E2E (선택)

14. **tmux 기반 실제 TUI 테스트**:
    ```
    Task(subagent_type="oh-my-claudecode:qa-tester", model="sonnet", prompt="
      TEST:
      Goal: verify TUI keyboard navigation and panel rendering
      Service: cd /Users/gkk/DEV/ockemon-pso && pnpm --filter @ockemon/cli build && node packages/cli/dist/index.js tui
      Test cases:
        1. TUI 시작 → 메뉴바 10개 항목 표시 확인
        2. Right arrow 2회 → 'Train' 하이라이트
        3. Enter → Train 패널 열림
        4. Esc → 메뉴로 복귀
        5. 'q' → 종료
    ")
    ```
</Steps>

<Tool_Usage>
## 핵심 도구

| 도구 | 용도 |
|------|------|
| Read | 소스/테스트 파일 읽기 |
| Glob | 테스트 파일 검색 |
| Grep | 패턴/mock 사용법 검색 |
| Write | 새 테스트 파일 생성 |
| Edit | 기존 테스트 수정 |
| Bash | `pnpm test` 실행 |
| Task | 에이전트 위임 (test-engineer, executor, architect, qa-tester, verifier) |

## 에이전트 라우팅

| Phase | 에이전트 | 모델 | 역할 |
|-------|----------|------|------|
| 설계 | test-engineer | sonnet | 테스트 케이스 목록 |
| 작성 | executor | sonnet | 테스트 코드 구현 |
| 진단 | architect | opus | 실패 근본 원인 |
| 수정 | executor | sonnet | 테스트 코드 수정 |
| E2E | qa-tester | sonnet | tmux 인터랙티브 |
| 검증 | verifier | sonnet | 완료 증거 |
</Tool_Usage>

<Examples>
<Good>
/tui-test use-menu
→ use-menu.ts 읽기 → 갭 분석 → 5개 테스트 설계 → 작성 → 실행 → PASS

/tui-test feed-panel --fix
→ feed-panel.tsx + feeding-game.test.tsx 분석 → 패널 래퍼 갭 식별 → 테스트 추가 → FAIL → 진단: mock 누락 → 수정 → PASS

/tui-test all
→ 전체 갭 분석 → 우선순위: use-menu → feed-panel → play-panel → ... → 순차 작성 → 전체 PASS

/tui-test --analyze
→ 갭 분석 결과만 출력 (코드 작성 없음)

/tui-test app --interactive
→ app.tsx 유닛 테스트 + tmux에서 실제 TUI 네비게이션 테스트
</Good>
<Bad>
/tui-test (인수 없이) → "무엇을 테스트할까요?" 질문으로 대응
/tui-test --build → "빌드 문제는 /build-fix 사용" 안내
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- 동일 실패 3회 연속 → 중단, "[TUI-TEST BLOCKED] {root cause}" 출력
- 최대 5사이클 도달 → 남은 실패 목록과 함께 중단
- 빌드 오류 발생 → "/build-fix 먼저 실행 필요" 안내
- 타입 오류 → "tsc 해결 필요" 안내
- 프로덕션 코드 버그 발견 → 사용자에게 알리고 별도 수정 제안
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] 대상의 모든 주요 경로(happy path, edge case) 테스트됨
- [ ] 기존 테스트 깨지지 않음 (전체 pnpm test 통과)
- [ ] mock 패턴이 프로젝트 기존 패턴과 일관
- [ ] 애니메이션 테스트에 vi.useFakeTimers() 사용
- [ ] stdin.write()로 키보드 상호작용 테스트됨
- [ ] afterEach에서 vi.restoreAllMocks() 호출
- [ ] import 경로에 .js 확장자 포함 (ESM)
</Final_Checklist>

<Test_Gap_Priority>
HIGH ROI (최우선):
1. app.tsx happy path — 전체 통합, 패널 전환, 가챠 오버레이
2. use-menu — 핵심 키보드 네비게이션
3. feed-panel + play-panel — 미니게임 게이트, 콜백 배선
4. use-streak + use-achievements — 사이드이펙트 로직

MEDIUM ROI:
5. stats-panel, dex-panel — 복합/페이지네이션 렌더링
6. use-gacha — DB + 애니메이션 상태머신
7. evolution-overlay — 애니메이션 컴포넌트

LOW ROI:
8. menu-bar, xp-bar, status-bars — 단순 프레젠테이셔널
9. reaction-patterns.ts — 순수 함수
10. use-interval — trivial 래퍼
</Test_Gap_Priority>
