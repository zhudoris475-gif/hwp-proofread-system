#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLAUDE 인스턴스 간 통신 채널 시스템
두 CLAUDE 인스턴스 간 메시지 공유를 위한 메시지 큐 시스템
"""

import json
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ClaudeChannel:
    """CLAUDE 인스턴스 간 통신 채널 클래스"""

    def __init__(self, channel_name: str = "claude_channel"):
        """
        채널 초기화

        Args:
            channel_name: 채널 이름 (기본값: "claude_channel")
        """
        self.channel_name = channel_name
        self.channel_dir = Path.home() / ".claude" / "channels" / channel_name
        self.channel_dir.mkdir(parents=True, exist_ok=True)

        # 메시지 큐 파일
        self.messages_file = self.channel_dir / "messages.json"
        self.status_file = self.channel_dir / "status.json"
        self.lock_file = self.channel_dir / "lock"

        # 메시지 저장소
        self.messages: List[Dict[str, Any]] = []
        self.status = {
            "last_message_time": None,
            "message_count": 0,
            "is_active": True,
            "participants": []
        }

        # 로드 메시지
        self._load_messages()
        self._load_status()

        # 메시지 수신 스레드 시작
        self._running = True
        self._receiver_thread = threading.Thread(target=self._receive_messages, daemon=True)
        self._receiver_thread.start()

    def _load_messages(self):
        """저장된 메시지 로드"""
        if self.messages_file.exists():
            try:
                with open(self.messages_file, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
            except Exception as e:
                print(f"[채널] 메시지 로드 실패: {e}")
                self.messages = []

    def _save_messages(self):
        """메시지 저장"""
        try:
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[채널] 메시지 저장 실패: {e}")

    def _load_status(self):
        """상태 로드"""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    self.status = json.load(f)
            except Exception as e:
                print(f"[채널] 상태 로드 실패: {e}")

    def _save_status(self):
        """상태 저장"""
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(self.status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[채널] 상태 저장 실패: {e}")

    def send_message(self, sender: str, content: str, message_type: str = "text",
                     metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        메시지 전송

        Args:
            sender: 발신자 ID
            content: 메시지 내용
            message_type: 메시지 타입 (text, command, alert, etc.)
            metadata: 추가 메타데이터

        Returns:
            전송 성공 여부
        """
        if not self._running:
            print("[채널] 채널이 비활성화되어 있습니다.")
            return False

        message = {
            "id": f"{sender}_{int(time.time())}_{len(self.messages)}",
            "sender": sender,
            "content": content,
            "message_type": message_type,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        try:
            self.messages.append(message)
            self._save_messages()

            # 상태 업데이트
            self.status["last_message_time"] = message["timestamp"]
            self.status["message_count"] = len(self.messages)
            self._save_status()

            print(f"[채널] 메시지 전송: {sender} → {message_type}")
            return True
        except Exception as e:
            print(f"[채널] 메시지 전송 실패: {e}")
            return False

    def receive_messages(self, sender: str) -> List[Dict[str, Any]]:
        """
        메시지 수신

        Args:
            sender: 수신자 ID

        Returns:
            수신된 메시지 리스트
        """
        received = []

        try:
            for msg in self.messages:
                if msg.get("sender") == sender:
                    received.append(msg)

            # 수신된 메시지 제거
            if received:
                self.messages = [msg for msg in self.messages if msg.get("sender") != sender]
                self._save_messages()

                # 상태 업데이트
                self.status["message_count"] = len(self.messages)
                self._save_status()

                print(f"[채널] 메시지 수신: {sender} → {len(received)}개 메시지")

            return received
        except Exception as e:
            print(f"[채널] 메시지 수신 실패: {e}")
            return []

    def _receive_messages(self):
        """메시지 수신 스레드 (백그라운드)"""
        while self._running:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def broadcast(self, content: str, message_type: str = "broadcast",
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        브로드캐스트 (모든 참여자에게 전송)

        Args:
            content: 메시지 내용
            message_type: 메시지 타입
            metadata: 추가 메타데이터

        Returns:
            전송 성공 여부
        """
        sender = "system"
        return self.send_message(sender, content, message_type, metadata)

    def get_recent_messages(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        최근 메시지 조회

        Args:
            count: 조회할 메시지 수

        Returns:
            최근 메시지 리스트
        """
        return self.messages[-count:] if self.messages else []

    def clear_messages(self) -> bool:
        """메시지 모두 삭제"""
        try:
            self.messages = []
            self._save_messages()
            self.status["message_count"] = 0
            self._save_status()
            print("[채널] 메시지가 모두 삭제되었습니다.")
            return True
        except Exception as e:
            print(f"[채널] 메시지 삭제 실패: {e}")
            return False

    def get_channel_info(self) -> Dict[str, Any]:
        """
        채널 정보 조회

        Returns:
            채널 정보 딕셔너리
        """
        return {
            "channel_name": self.channel_name,
            "channel_dir": str(self.channel_dir),
            "message_count": len(self.messages),
            "last_message_time": self.status.get("last_message_time"),
            "status": self.status,
            "participants": self.status.get("participants", [])
        }

    def add_participant(self, participant_id: str) -> bool:
        """
        참여자 추가

        Args:
            participant_id: 참여자 ID

        Returns:
            추가 성공 여부
        """
        participants = self.status.get("participants", [])
        if participant_id not in participants:
            participants.append(participant_id)
            self.status["participants"] = participants
            self._save_status()
            print(f"[채널] 참여자 추가: {participant_id}")
            return True
        return False

    def remove_participant(self, participant_id: str) -> bool:
        """
        참여자 제거

        Args:
            participant_id: 참여자 ID

        Returns:
            제거 성공 여부
        """
        participants = self.status.get("participants", [])
        if participant_id in participants:
            participants.remove(participant_id)
            self.status["participants"] = participants
            self._save_status()
            print(f"[채널] 참여자 제거: {participant_id}")
            return True
        return False

    def close(self):
        """채널 닫기"""
        self._running = False
        if self._receiver_thread.is_alive():
            self._receiver_thread.join(timeout=2)
        print(f"[채널] 채널 '{self.channel_name}'이 닫혔습니다.")


# 채널 매니저 (싱글톤)
_channel_manager: Optional[ClaudeChannel] = None


def get_channel(channel_name: str = "claude_channel") -> ClaudeChannel:
    """
    채널 매니저 가져오기 (싱글톤)

    Args:
        channel_name: 채널 이름

    Returns:
        ClaudeChannel 인스턴스
    """
    global _channel_manager
    if _channel_manager is None:
        _channel_manager = ClaudeChannel(channel_name)
    return _channel_manager


if __name__ == "__main__":
    # 테스트 코드
    print("CLAUDE 채널 시스템 테스트 시작...")

    # 채널 생성
    channel = get_channel("test_channel")

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
    print(json.dumps(info, ensure_ascii=False, indent=2))

    # 채널 닫기
    channel.close()
    print("\n테스트 완료!")
