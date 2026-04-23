# CLAUDE 인스턴스 간 통신 채널 시스템

## 개요

이 시스템은 두 CLAUDE 인스턴스 간 메시지 공유를 위한 통신 채널을 제공합니다.

## 주요 기능

1. **메시지 전송/수신**: 두 CLAUDE 인스턴스 간 실시간 메시지 전송
2. **브로드캐스트**: 모든 참여자에게 메시지 전송
3. **참여자 관리**: 채널에 참여하는 인스턴스 관리
4. **메시지 큐**: 메시지를 영구적으로 저장하고 관리
5. **메타데이터**: 메시지에 추가 정보 포함

## 설치

```bash
# 채널 시스템 스크립트 위치
~/.agent-skills/claude_channel.py

# 테스트 스크립트 위치
~/.agent-skills/test_channel.py
```

## 사용법

### 1. 기본 사용

```python
from claude_channel import ClaudeChannel

# 채널 생성
channel = ClaudeChannel("my_channel")

# 참여자 추가
channel.add_participant("claude_1")
channel.add_participant("claude_2")

# 메시지 전송
channel.send_message("claude_1", "안녕하세요!", "text")

# 메시지 수신
received = channel.receive_messages("claude_1")
for msg in received:
    print(f"{msg['sender']}: {msg['content']}")
```

### 2. 브로드캐스트

```python
# 모든 참여자에게 메시지 전송
channel.broadcast("중요 공지입니다.", "broadcast")
```

### 3. 최근 메시지 조회

```python
# 최근 10개 메시지 조회
recent = channel.get_recent_messages(10)
```

### 4. 채널 정보 조회

```python
# 채널 정보
info = channel.get_channel_info()
print(f"메시지 수: {info['message_count']}")
print(f"참여자: {info['participants']}")
```

## 메시지 타입

- `text`: 일반 텍스트 메시지
- `command`: 명령 메시지
- `alert`: 알림 메시지
- `broadcast`: 브로드캐스트 메시지
- `data`: 데이터 전송 메시지

## 파일 구조

```
~/.claude/channels/
└── claude_channel/          # 기본 채널
    ├── messages.json        # 메시지 저장소
    ├── status.json          # 채널 상태
    └── lock                 # 잠금 파일
```

## 테스트

```bash
# 테스트 실행
python test_channel.py
```

## CLAUDE 인스턴스 통합

### CLAUDE 1 (메시지 발신)

```python
import claude_channel

channel = claude_channel.ClaudeChannel("claude_channel")
channel.add_participant("claude_1")
channel.send_message("claude_1", "작업 완료했습니다!", "command")
```

### CLAUDE 2 (메시지 수신)

```python
import claude_channel

channel = claude_channel.ClaudeChannel("claude_channel")
channel.add_participant("claude_2")

# 메시지 수신
for msg in channel.receive_messages("claude_2"):
    if msg['message_type'] == 'command':
        print(f"명령 수신: {msg['content']}")
```

## 주의사항

1. 채널 이름이 같아야 두 인스턴스가 통신 가능
2. 메시지는 영구적으로 저장되므로 주기적으로 정리 필요
3. 동일한 참여자 ID에서 메시지를 수신하면 자동 삭제

## 확장 기능

- 메시지 암호화
- 메시지 만료 시간 설정
- 파일 전송 지원
- 실시간 알림 (WebSocket 등)

## 예제

두 CLAUDE 인스턴스가 공동 작업을 수행하는 예제:

```python
# CLAUDE 1: 작업 시작
channel = ClaudeChannel("collaboration")
channel.send_message("claude_1", "프로젝트 시작", "broadcast")

# CLAUDE 2: 작업 수행
channel.send_message("claude_2", "작업 중입니다...", "text")

# CLAUDE 1: 상태 확인
channel.send_message("claude_1", "진행 상황 확인", "command")

# CLAUDE 2: 응답
channel.send_message("claude_2", "90% 완료", "text")

# CLAUDE 1: 완료 알림
channel.send_message("claude_1", "프로젝트 완료!", "broadcast")
```

---

**버전**: 1.0.0
**작성일**: 2026-04-19
**작성자**: Claude
