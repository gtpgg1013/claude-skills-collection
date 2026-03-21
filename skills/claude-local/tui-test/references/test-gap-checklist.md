# TUI Test Gap Checklist

## HIGH ROI

### 1. app.tsx happy path
- [ ] ockemon 존재 시 전체 렌더링 (SpriteCanvas, XpBar, StatusBars, StreakBar, MenuBar)
- [ ] 패널 전환: Right arrow → Enter → 패널 열림 → Esc → 메뉴 복귀
- [ ] 가챠 오버레이 테이크오버 (isAnimating=true 시 패널 대신 GachaOverlay)
- [ ] 터미널 사이즈 가드 (columns < 60 또는 rows < 16 시 경고)
- [ ] q/Esc 종료 동작
- [ ] 리액션 시스템 (triggerReaction 후 애니메이션)

### 2. use-menu
- [ ] 초기 상태: selectedIndex=0, activePanel=null
- [ ] Right arrow → selectedIndex 증가 (0→1→2...→9→0 순환)
- [ ] Left arrow → selectedIndex 감소 (0→9→8... 순환)
- [ ] Enter → activePanel 설정 (PANEL_MAP[selectedIndex])
- [ ] Esc/Back → activePanel=null
- [ ] 패널 열린 상태에서 ←/→ 무시

### 3. feed-panel
- [ ] 초기 렌더: 일일 횟수 표시 (getDailyCount)
- [ ] 미니게임 게이트: minigame_enabled 설정에 따라 FeedingGame 또는 즉시 피드
- [ ] FeedingGame 완료 후 onFed 콜백 → activityRepo.insert
- [ ] 일일 한도 도달 시 비활성

### 4. play-panel
- [ ] 초기 렌더: 일일 횟수 표시
- [ ] RhythmGame 완료 후 onPlayed 콜백
- [ ] 일일 한도 도달 시 비활성

### 5. use-streak
- [ ] 마일스톤 감지: streak가 7, 30, 100, 365 통과 시 toast 발동
- [ ] 스트릭 변경 없으면 toast 없음
- [ ] addToast 호출 확인

### 6. use-achievements
- [ ] 첫 렌더 시 toast 발동 안 함 (isFirstRef.current=true)
- [ ] 두 번째 렌더에서 새 언락 감지 → toast
- [ ] hidden 업적도 언락 시 toast
- [ ] 변경 없으면 toast 없음

## MEDIUM ROI

### 7. stats-panel
- [ ] TendencyRadar + AchievementGrid + PersonalityBadge 복합 렌더
- [ ] ockemon 없을 때 빈 상태

### 8. dex-panel
- [ ] 페이지네이션: ←/→ 페이지 이동
- [ ] 그리드 레이아웃: columns 기반
- [ ] discoveredCount / totalCount 표시

### 9. use-gacha
- [ ] pendingBoxes 읽기 (configRepo)
- [ ] rollRewardBox → GachaResult 생성
- [ ] dismiss → configRepo 업데이트
- [ ] 박스 없으면 null 반환

### 10. evolution-overlay.tsx
- [ ] 5단계 프레임 렌더링 (flash→fadeOut→white→fadeIn→celebrate)
- [ ] onComplete 콜백 호출

## LOW ROI

### 11. menu-bar
- [ ] selectedIndex 하이라이트
- [ ] disabled 상태 (패널 열림 시)
- [ ] columns >= 70 일 때 힌트 텍스트

### 12. xp-bar, status-bars, personality-badge
- [ ] props → 올바른 텍스트 렌더

### 13. reaction-patterns.ts
- [ ] getReactionFrames('feed') 반환 확인
- [ ] getReactionFrames('play') 반환 확인

### 14. use-interval
- [ ] callback이 ms 간격으로 호출됨
