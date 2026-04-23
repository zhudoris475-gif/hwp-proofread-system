#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLAUDE 인스턴스 간 협업 예제
두 CLAUDE 인스턴스가 공동 작업을 수행하는 시나리오
"""

import sys
import io
import time
import threading

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import claude_channel


class ClaudeInstance:
    """CLAUDE 인스턴스 클래스"""

    def __init__(self, instance_id: str, channel_name: str = "claude_channel"):
        """
        인스턴스 초기화

        Args:
            instance_id: 인스턴스 ID
            channel_name: 채널 이름
        """
        self.instance_id = instance_id
        self.channel = claude_channel.ClaudeChannel(channel_name)
        self.channel.add_participant(instance_id)

        # 작업 상태
        self.current_task = None
        self.task_progress = 0
        self.is_working = False

    def send_status(self, status: str, progress: int = None):
        """상태 전송"""
        metadata = {"progress": progress} if progress is not None else {}
        self.channel.send_message(
            self.instance_id,
            f"상태: {status}",
            "text",
            metadata
        )

    def send_task_update(self, task: str, status: str):
        """작업 업데이트 전송"""
        self.channel.send_message(
            self.instance_id,
            f"작업 [{task}]: {status}",
            "command"
        )

    def receive_messages(self):
        """메시지 수신 및 처리"""
        print(f"[{self.instance_id}] 메시지 수신 대기 중...")

        while True:
            received = self.channel.receive_messages(self.instance_id)

            for msg in received:
                print(f"[{self.instance_id}] 수신: {msg['sender']} → {msg['content']}")

                # 메시지 처리
                if msg['message_type'] == 'command':
                    self._process_command(msg)
                elif msg['message_type'] == 'broadcast':
                    print(f"[{self.instance_id}] 공지: {msg['content']}")
                elif msg['message_type'] == 'alert':
                    print(f"[{self.instance_id}] 알림: {msg['content']}")

            time.sleep(1)

    def _process_command(self, msg: dict):
        """명령 처리"""
        content = msg['content']

        if "시작" in content or "시작하라" in content:
            self.start_task()
        elif "중지" in content or "멈춰라" in content:
            self.stop_task()
        elif "진행 상황" in content:
            self.report_progress()

    def start_task(self):
        """작업 시작"""
        if self.is_working:
            print(f"[{self.instance_id}] 이미 작업 중입니다.")
            return

        self.is_working = True
        self.current_task = "자동화 작업"
        self.task_progress = 0

        self.channel.broadcast(
            f"[{self.instance_id}] 작업 시작: {self.current_task}",
            "broadcast"
        )
        self.send_status("작업 시작", 0)

        # 작업 시뮬레이션
        self._simulate_work()

    def _simulate_work(self):
        """작업 시뮬레이션"""
        for i in range(1, 11):
            if not self.is_working:
                break

            time.sleep(1)
            self.task_progress = i * 10
            self.send_status("작업 진행 중...", self.task_progress)

        if self.is_working:
            self.complete_task()

    def stop_task(self):
        """작업 중지"""
        if not self.is_working:
            print(f"[{self.instance_id}] 작업 중이 아닙니다.")
            return

        self.is_working = False
        self.channel.broadcast(
            f"[{self.instance_id}] 작업 중지됨",
            "broadcast"
        )
        self.send_status("작업 중지됨")

    def complete_task(self):
        """작업 완료"""
        self.is_working = False
        self.channel.broadcast(
            f"[{self.instance_id}] 작업 완료! 진행률: {self.task_progress}%",
            "broadcast"
        )
        self.send_status("작업 완료", 100)

    def report_progress(self):
        """진행 상황 보고"""
        self.send_status(
            f"진행 상황 보고 (현재 진행률: {self.task_progress}%)",
            self.task_progress
        )


def main():
    print("=== CLAUDE 인스턴스 간 협업 예제 ===\n")

    # 두 인스턴스 생성
    claude_1 = ClaudeInstance("claude_1")
    claude_2 = ClaudeInstance("claude_2")

    # 메시지 수신 스레드 시작
    receiver_thread = threading.Thread(
        target=claude_1.receive_messages,
        daemon=True
    )
    receiver_thread.start()

    # 5초 대기 후 작업 시작
    print("5초 후 작업 시작...\n")
    time.sleep(5)

    # CLAUDE 1이 작업 시작
    print("CLAUDE 1: 작업 시작 명령 전송\n")
    claude_1.start_task()

    # CLAUDE 2가 작업 모니터링
    print("CLAUDE 2: 메시지 수신 대기 중...\n")
    time.sleep(8)

    # 작업 중지
    print("\nCLAUDE 1: 작업 중지 명령 전송\n")
    claude_1.stop_task()

    # 작업 완료
    print("\nCLAUDE 1: 작업 완료 알림\n")
    claude_1.complete_task()

    # 채널 닫기
    claude_1.channel.close()
    claude_2.channel.close()

    print("\n=== 예제 완료 ===")


if __name__ == "__main__":
    main()
