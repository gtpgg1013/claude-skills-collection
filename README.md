# Claude Skills & Plugins Collection

이 PC에 설치된 Claude Code 스킬과 플러그인을 종합 정리한 레포지토리입니다.

## 구조

```
skills/
├── agents/          # ~/.agents/skills/ (공유 스킬 - 37개)
├── claude-local/    # ~/.claude/skills/ (로컬 전용 스킬 - 5개)
└── plugins/         # ~/.claude/plugins/ (플러그인 스킬)
    ├── superpowers/ # Anthropic 공식 (14개 스킬)
    ├── gptaku/      # fivetaku/gptaku_plugins (9개 플러그인, 21개 스킬)
    └── omc/         # oh-my-claudecode (36개 스킬)
```

---

## 마켓플레이스 (Plugin Sources)

| 마켓플레이스 | 소스 | 설명 |
|-------------|------|------|
| **claude-plugins-official** | `anthropics/claude-plugins-official` | Anthropic 공식 플러그인 |
| **gptaku-plugins** | `fivetaku/gptaku_plugins` | 한국어 중심 AI 도구 모음 |
| **omc** | `Yeachan-Heo/oh-my-claudecode` | Claude Code 확장 프레임워크 |

---

## 1. Superpowers (Anthropic 공식) — 14개 스킬

개발 워크플로우 전반을 체계화하는 공식 플러그인.

| 스킬 | 설명 |
|------|------|
| **using-superpowers** | 대화 시작 시 스킬 탐색/활성화 확립 |
| **brainstorming** | 구현 전 사용자 의도·요구사항·설계 탐색 |
| **writing-plans** | 스펙/요구사항 기반 멀티스텝 작업 계획 수립 |
| **executing-plans** | 작성된 구현 계획을 리뷰 체크포인트와 함께 실행 |
| **test-driven-development** | 기능/버그픽스 구현 전 테스트 우선 작성 |
| **systematic-debugging** | 버그·테스트 실패·예상치 못한 동작 체계적 디버깅 |
| **subagent-driven-development** | 독립 태스크를 서브에이전트로 병렬 실행 |
| **dispatching-parallel-agents** | 2개 이상 독립 작업 병렬 처리 |
| **using-git-worktrees** | 격리된 git worktree에서 피처 작업 |
| **finishing-a-development-branch** | 구현 완료 후 머지/PR/정리 옵션 제시 |
| **requesting-code-review** | 작업 완료·주요 기능 구현 후 검증 요청 |
| **receiving-code-review** | 코드 리뷰 피드백 수신 시 기술적 검증 |
| **verification-before-completion** | 완료 선언 전 검증 명령 실행·증거 확인 |
| **writing-skills** | 새 스킬 생성·수정·배포 전 검증 |

---

## 2. gptaku-plugins (fivetaku) — 9개 플러그인

### git-teacher (깃선생) — 6개 스킬
Git/GitHub를 한국어로 쉽게 안내하는 도구.

| 스킬 | 설명 | 트리거 |
|------|------|--------|
| **git-teacher-setup** | Git/GitHub 초기 설정·프로젝트 폴더 생성 | "깃 시작", "깃 설정", "처음이에요" |
| **git-teacher-status** | Git 상태를 한국어 자연어로 번역 | "상태 확인", "뭐가 바뀌었어?" |
| **git-teacher-save** | 변경 파일 커밋 | "저장해줘", "커밋해줘" |
| **git-teacher-upload** | GitHub에 Push | "올려줘", "푸시", "업로드" |
| **git-teacher-review** | Branch → PR 자동 생성 | "PR 만들어줘", "검토 요청" |
| **git-teacher-help** | Git 용어를 클라우드 비유로 설명 | "commit이 뭐야?", "깃 용어" |

### vibe-sunsang (바선생) — 5개 스킬
AI 활용 성장 멘토 에이전트.

| 스킬 | 설명 |
|------|------|
| **vibe-sunsang-onboard** | 초기 설정·프로젝트 연결·첫 변환 안내 |
| **vibe-sunsang-mentor** | AI 활용 능력 코칭 (4가지 모드) |
| **vibe-sunsang-knowledge** | 용어·레벨 시스템·안티패턴 지식 베이스 |
| **vibe-sunsang-retro** | Claude Code 대화 로그 → Markdown 변환 |
| **vibe-sunsang-growth** | 세션 데이터 분석 → 성장 리포트 생성 |

### deep-research (딥리서치) — 2개 스킬
멀티에이전트 기반 종합 리서치 시스템.

| 스킬 | 설명 |
|------|------|
| **deep-research-main** | 주제별 딥리서치 실행 |
| **deep-research-query** | 구조화된 리서치 쿼리 빌더 |

### 단일 스킬 플러그인

| 플러그인 | 스킬 | 설명 |
|---------|------|------|
| **show-me-the-prd** | show-me-the-prd | 인터뷰 기반 PRD 생성 (4종 디자인 문서) |
| **docs-guide** | docs-guide-knowledge | 공식 문서 검색/설명 (llms.txt 기반) |
| **kkirikkiri** | kkirikkiri | 자연어로 AI 에이전트 팀 자동 구성·실행 |
| **pumasi** | pumasi | Codex CLI를 병렬 외주 개발자로 활용 |
| **skillers-suda** | skillers-suda | 4명의 전문가가 아이디어 → 스킬 변환 |
| **nopal** | nopal-orchestrate / nopal-setup | Google Workspace 9개 서비스 오케스트레이션 |

---

## 3. oh-my-claudecode (OMC) — 36개 스킬

Claude Code 확장 프레임워크. 자율 실행, 팀 오케스트레이션, 코드 리뷰 등.

### 핵심 실행 모드

| 스킬 | 설명 |
|------|------|
| **autopilot** | 아이디어 → 동작 코드까지 완전 자율 실행 |
| **ralph** | 태스크 완료까지 자기참조 루프 + 아키텍트 검증 |
| **ultrawork** | 고처리량 태스크 병렬 실행 엔진 |
| **ultrapilot** | 파일 소유권 파티셔닝 기반 병렬 autopilot |
| **ultraqa** | QA 사이클링 — 테스트·검증·수정 반복 |
| **cancel** | 활성 모드 취소 |

### 플래닝 & 분석

| 스킬 | 설명 |
|------|------|
| **plan** | 인터뷰 워크플로우 포함 전략적 플래닝 |
| **ralplan** | /plan --consensus 별칭 |
| **review** | /plan --review 별칭 |
| **ralph-init** | 구조화된 ralph-loop 실행을 위한 PRD 초기화 |
| **analyze** | 심층 분석·조사 |
| **deepinit** | 계층적 AGENTS.md 문서화 기반 코드베이스 초기화 |

### 팀 & 오케스트레이션

| 스킬 | 설명 |
|------|------|
| **team** | Claude Code 네이티브 팀 — N개 에이전트 조율 |
| **omc-teams** | tmux 패인에 claude/codex/gemini 워커 스폰 |
| **ccg** | Claude-Codex-Gemini 3모델 오케스트레이션 |
| **worker** | 팀 워커 프로토콜 (ACK, 메일박스, 태스크 라이프사이클) |
| **pipeline** | 에이전트 체이닝 — 순차/분기 워크플로우 |
| **sciomc** | 병렬 과학자 에이전트 오케스트레이션 + AUTO 모드 |

### 코드 품질

| 스킬 | 설명 |
|------|------|
| **code-review** | 종합 코드 리뷰 |
| **security-review** | 종합 보안 리뷰 |
| **tdd** | 테스트 주도 개발 강제 |
| **build-fix** | 빌드/TypeScript 에러 최소 변경으로 수정 |

### 유틸리티 & 설정

| 스킬 | 설명 |
|------|------|
| **omc-setup** | oh-my-claudecode 설정 (유일하게 알면 되는 커맨드) |
| **omc-help** | 사용 가이드 |
| **omc-doctor** | 설치 문제 진단·수정 |
| **skill** | 로컬 스킬 관리 — 목록, 추가, 제거, 검색, 편집 |
| **hud** | HUD 디스플레이 설정 |
| **note** | notepad.md에 노트 저장 (컴팩션 복원력) |
| **trace** | 에이전트 플로우 트레이스 타임라인·요약 |
| **configure-notifications** | 알림 통합 설정 (Telegram, Discord, Slack) |
| **mcp-setup** | MCP 서버 설정 |
| **learn-about-omc** | 사용 패턴 학습·맞춤 추천 |
| **learner** | 현재 대화에서 학습된 스킬 추출 |
| **release** | oh-my-claudecode 자동 릴리스 워크플로우 |
| **project-session-manager** | git worktree + tmux 세션 격리 환경 관리 |

### 외부 연동

| 스킬 | 설명 |
|------|------|
| **ask-claude** | Claude CLI 호출 → 재사용 가능 아티팩트 캡처 |
| **ask-gemini** | Gemini CLI 호출 → 재사용 가능 아티팩트 캡처 |
| **external-context** | 병렬 문서 전문가 에이전트로 웹 검색·문서 조회 |
| **writer-memory** | 작가용 에이전틱 메모리 (캐릭터, 관계, 장면, 테마) |

---

## 4. 공유 스킬 (~/.agents/skills/) — 37개

OMC에서 설치된 스킬들로, `~/.claude/skills/`에 심볼릭 링크로 연결.

### UI/UX & 디자인

| 스킬 | 설명 |
|------|------|
| **ui-ux-pro-max** | UI/UX 디자인 인텔리전스 (glassmorphism, 다크모드 등) |
| **design-taste-frontend** | 시니어 UI/UX 엔지니어 — LLM 기본 바이어스 오버라이드 |
| **gsap-fundamentals** | GSAP 애니메이션 기초 (트윈, 타임라인, 이징) |

### 레트로 & 픽셀아트

| 스킬 | 설명 |
|------|------|
| **8-bit-pixel-art-patterns** | 8비트 레트로 UI 픽셀 아트 패턴 |
| **pixel-art-sprites** | 픽셀 아트·스프라이트 애니메이션 제작 |
| **retro-css-architecture** | 8비트 CSS 아키텍처 (커스텀 프로퍼티, 픽셀 폰트) |
| **rendering-animate-svg** | SVG 애니메이션 하드웨어 가속 래핑 |

### 테스팅

| 스킬 | 설명 |
|------|------|
| **dogfood** | 웹앱 탐색적 테스팅·QA·버그 헌팅 |
| **playwright-e2e-testing** | Playwright E2E 테스트 (크로스 브라우저, 오토웨이트) |
| **visual-regression-testing** | 시각적 회귀 테스트 (스크린샷 diff) |
| **visual-verdict** | 스크린샷 vs 레퍼런스 구조화된 QA 판정 |
| **tui-visual-qa** | 터미널 UI QA (tmux 세션, 키보드 시나리오, 스크린샷) |

### 자율 실행 & 플래닝

| 스킬 | 설명 |
|------|------|
| **autopilot** | 아이디어 → 동작 코드 완전 자율 실행 |
| **ralph** | 태스크 완료까지 자기참조 루프 |
| **ultrawork** | 고처리량 병렬 실행 엔진 |
| **plan** | 인터뷰 워크플로우 전략적 플래닝 |
| **ralplan** | /plan --consensus 별칭 |
| **deep-interview** | 소크라테스식 심층 인터뷰 + 수학적 모호성 게이팅 |

### 코드 품질 & 보안

| 스킬 | 설명 |
|------|------|
| **code-review** | 종합 코드 리뷰 |
| **security-review** | 종합 보안 리뷰 |
| **ai-slop-cleaner** | AI 슬롭 클린업/리팩터 워크플로우 |

### 팀 & 오케스트레이션

| 스킬 | 설명 |
|------|------|
| **team** | N개 에이전트 tmux 기반 조율 |
| **worker** | 팀 워커 프로토콜 |

### 유틸리티

| 스킬 | 설명 |
|------|------|
| **find-skills** | 스킬 검색·설치 도우미 |
| **skill** | 로컬 스킬 관리 |
| **help** | oh-my-codex 사용 가이드 |
| **doctor** | 설치 문제 진단·수정 |
| **omx-setup** | oh-my-codex 설정 |
| **note** | 노트 저장 (컴팩션 복원력) |
| **trace** | 에이전트 플로우 트레이스 |
| **hud** | HUD 상태라인 설정 |
| **cancel** | 활성 모드 취소 |
| **configure-notifications** | 알림 설정 |
| **powerpoint** | PowerPoint 생성·디자인·분석 |
| **web-clone** | URL 기반 웹사이트 클로닝 (시각+기능 검증) |
| **ask-claude** | Claude CLI 호출·아티팩트 캡처 |
| **ask-gemini** | Gemini CLI 호출·아티팩트 캡처 |

---

## 5. 로컬 전용 스킬 (~/.claude/skills/) — 5개

프로젝트 특화 스킬 (ockemon-pso 프로젝트용).

| 스킬 | 설명 |
|------|------|
| **minecraft-3d-avatar** | Minecraft 스타일 3D 블록 캐릭터 아바타 (React Three Fiber) |
| **team-dogfood** | /team 파이프라인 + 병렬 브라우저 QA |
| **team-tui** | /team 파이프라인 + 병렬 TUI 테스트 QA |
| **tui-test** | TUI 컴포넌트·훅 테스트 (ink-testing-library + vitest) |
| **tui-visual-test** | TUI 시각 테스트 (렌더링 스냅샷, 프레임 비교) |

---

## 전체 통계

| 카테고리 | 개수 |
|---------|------|
| Superpowers (공식) | 14 스킬 |
| gptaku-plugins | 9 플러그인 / 21 스킬 |
| oh-my-claudecode | 36 스킬 |
| 공유 스킬 (agents) | 37개 |
| 로컬 전용 스킬 | 5개 |

> 참고: 공유 스킬(agents)과 OMC 플러그인 스킬은 상당 부분 중복됩니다 (OMC 설치 시 agents 폴더에도 복사됨).
