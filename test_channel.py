#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLAUDE 채널 테스트 스크립트
"""

import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 채널 시스템 임포트
import claude_channel

def main():
    print("CLAUDE 채널 시스템 테스트 시작...")

    # 채널 생성
    channel = claude_channel.ClaudeChannel("test_channel")

    # 참여자 추가
    channel.add_participant("claude_1")
    channel.add_participant("claude_2")

    # 메시지 전송 테스트
    print("\n=== 메시지 전송 테스트 ===")
    channel.send_message("claude_1", "안녕하세요! CLAUDE 1입니다.", "text")
    channel.send_message("claude_2", "안녕! CLAUDE 2입니다. 반가워요.", "text")
    channel.broadcast("모두에게 공지: 채널 테스트 시작", "broadcast")

    # 메시지 수신 테스트
    print("\n=== 메시지 수신 테스트 ===")
    received = channel.receive_messages("claude_1")
    print(f"CLAUDE 1 수신 메시지: {len(received)}개")
    for msg in received:
        print(f"  - [{msg['timestamp']}] {msg['sender']}: {msg['content']}")

    # 최근 메시지 조회
    print("\n=== 최근 메시지 ===")
    recent = channel.get_recent_messages(5)
    for msg in recent:
        print(f"  - [{msg['timestamp']}] {msg['sender']}: {msg['content']}")

    # 채널 정보
    print("\n=== 채널 정보 ===")
    info = channel.get_channel_info()
    print(f"채널 이름: {info['channel_name']}")
    print(f"메시지 수: {info['message_count']}")
    print(f"마지막 메시지 시간: {info['last_message_time']}")
    print(f"참여자: {info['participants']}")

    # 채널 닫기
    channel.close()
    print("\n테스트 완료!")

if __name__ == "__main__":
    main()
