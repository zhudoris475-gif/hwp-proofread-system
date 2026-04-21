#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3개 CLAUDE 인스턴스 통신 테스트
"""

import sys
import io
import time
import threading

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import claude_channel


def test_three_instances():
    """3개 인스턴스 통신 테스트"""
    print("=== 3개 CLAUDE 인스턴스 통신 테스트 ===\n")

    # 3개 인스턴스 생성 (같은 채널 이름 사용)
    channel = claude_channel.ClaudeChannel("multi_channel")
    claude_1 = channel
    claude_2 = channel
    claude_3 = channel

    # 참여자 추가
    claude_1.add_participant("claude_1")
    claude_2.add_participant("claude_2")
    claude_3.add_participant("claude_3")

    print("✅ 3개 인스턴스가 같은 채널에 참여했습니다.\n")

    # 메시지 전송 스레드 함수
    def sender_1():
        time.sleep(2)
        print("[CLAUDE 1] 메시지 전송 시작...")
        claude_1.send_message("claude_1", "안녕하세요! CLAUDE 1입니다.", "text")

        time.sleep(2)
        claude_1.send_message("claude_1", "작업을 시작합니다.", "command")

        time.sleep(3)
        claude_1.send_message("claude_1", "진행률: 50%", "text")

        time.sleep(3)
        claude_1.send_message("claude_1", "진행률: 100% 완료!", "broadcast")

    def sender_2():
        time.sleep(1)
        print("[CLAUDE 2] 메시지 수신 대기 중...")
        received = claude_2.receive_messages("claude_2")

        print(f"[CLAUDE 2] 수신된 메시지: {len(received)}개")
        for msg in received:
            print(f"  - [{msg['timestamp']}] {msg['sender']}: {msg['content']}")

        time.sleep(2)
        claude_2.send_message("claude_2", "CLAUDE 2가 확인했습니다.", "text")

    def sender_3():
        time.sleep(4)
        print("[CLAUDE 3] 메시지 수신 대기 중...")
        received = claude_3.receive_messages("claude_3")

        print(f"[CLAUDE 3] 수신된 메시지: {len(received)}개")
        for msg in received:
            print(f"  - [{msg['timestamp']}] {msg['sender']}: {msg['content']}")

        time.sleep(2)
        claude_3.send_message("claude_3", "모두 감사합니다!", "broadcast")

    # 스레드 시작
    threads = [
        threading.Thread(target=sender_1, daemon=True),
        threading.Thread(target=sender_2, daemon=True),
        threading.Thread(target=sender_3, daemon=True)
    ]

    for t in threads:
        t.start()

    # 대기
    for t in threads:
        t.join(timeout=15)

    # 채널 닫기
    channel.close()

    print("\n=== 테스트 완료 ===")


if __name__ == "__main__":
    test_three_instances()
