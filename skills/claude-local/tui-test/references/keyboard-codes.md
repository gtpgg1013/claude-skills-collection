# Keyboard Codes — stdin.write() Reference

## Navigation Keys

| Key | Code | Usage |
|-----|------|-------|
| Enter | `'\r'` | 메뉴 선택, 확인 |
| Escape | `'\x1B'` | 패널 닫기, 취소 |
| Up Arrow | `'\x1B[A'` | 목록 위로 |
| Down Arrow | `'\x1B[B'` | 목록 아래로 |
| Right Arrow | `'\x1B[C'` | 메뉴 오른쪽 |
| Left Arrow | `'\x1B[D'` | 메뉴 왼쪽 |
| Tab | `'\t'` | 다음 항목 |
| Backspace | `'\x7F'` | 입력 삭제 |
| Space | `' '` | 토글/선택 |

## Character Keys

| Key | Code |
|-----|------|
| q | `'q'` |
| y | `'y'` |
| n | `'n'` |
| 1-9 | `'1'` ~ `'9'` |

## Modifier Keys

| Key | Code |
|-----|------|
| Ctrl+C | `'\x03'` |
| Ctrl+D | `'\x04'` |
| Ctrl+Z | `'\x1A'` |

## Example: Menu Navigation

```typescript
const { stdin, lastFrame } = render(<App />);

// Move right 2 times (Feed → Play → Train)
stdin.write('\x1B[C');
stdin.write('\x1B[C');

// Select current menu item
stdin.write('\r');

// Go back to menu
stdin.write('\x1B');

// Quit
stdin.write('q');
```

## Example: Minigame Input

```typescript
// Feeding game: Enter to capture timing
stdin.write('\r');

// Rhythm game: Arrow pattern
stdin.write('\x1B[A'); // Up
stdin.write('\x1B[D'); // Left
stdin.write('\x1B[C'); // Right
stdin.write('\x1B[B'); // Down
```

## Important Notes

- `stdin.write()` 후 useEffect flush 필요:
  ```typescript
  stdin.write('\r');
  await new Promise(r => setTimeout(r, 10));
  ```
- useInput은 Ink의 raw mode에서 동작 — ink-testing-library가 자동 처리
- 여러 키 연속 입력 시 각각 별도 write() 호출
