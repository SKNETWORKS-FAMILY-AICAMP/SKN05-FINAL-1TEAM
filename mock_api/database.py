from datetime import datetime
from typing import Dict, List, Optional
import random
import jwt
import hashlib
import asyncio

# Mock database
class MockDB:
    def __init__(self):
        self.users = {
            "test@example.com": {
                "username": "테스트유저",
                "password": self._hash_password("test1234"),  # 실제 서비스에서는 더 안전한 해시 방식 사용
                "email": "test@example.com",
                "userId": 12345,
                "created_at": "2024-03-01T00:00:00"
            },
            "camera@example.com": {
                "username": "카메라매니아",
                "password": self._hash_password("camera1234"),
                "email": "camera@example.com",
                "userId": 12346,
                "created_at": "2024-03-15T00:00:00"
            }
        }
        self.sessions: Dict[int, List[dict]] = {}  # userId를 key로 사용
        self.chat_messages: Dict[int, List[dict]] = {}  # sessionId를 key로 사용
        self.current_session_id = 1  # 1부터 시작
        self.current_message_id = 1
        self._current_session_id = None  # 현재 세션 ID 저장
        self.keywords_db = {
            "Python워크": "소프트웨어 개발을 위한 기본 구조와 도구들을 제공하는 플랫폼입니다. 개발자가 핵심 기능 구현에 집중할 수 있도록 도와줍니다.",
            "DSLR": "Digital Single-Lens Reflex의 약자로, 디지털 일안 반사식 카메라입니다. 렌즈를 통해 들어온 빛이 반사거울에 반사되어 뷰파인더로 전달되는 방식의 카메라입니다.",
            "미러리스": "반사거울이 없는 디지털 카메라로, DSLR보다 작고 가벼운 것이 특징입니다. 최근에는 성능면에서도 DSLR과 대등하거나 뛰어난 제품들이 많습니다.",
            "조리개": "카메라 렌즈에서 빛이 통과하는 구멍의 크기를 조절하는 장치입니다. F값으로 표시되며, 피사계 심도와 밝기를 조절하는 중요한 요소입니다.",
            "셔터스피드": "카메라의 셔터가 열려있는 시간을 의미합니다. 빠른 셔터스피드는 움직이는 피사체를 선명하게 촬영할 수 있고, 느린 셔터스피드는 움직임을 표현할 수 있습니다.",
            "ISO": "이미지 센서의 빛 감도를 나타내는 수치입니다. 높은 ISO는 어두운 환경에서 촬영이 가능하지만, 노이즈가 증가할 수 있습니다.",
            "RAW": "카메라 센서가 캡처한 모든 이미지 데이터를 포함하는 파일 형식입니다. JPEG보다 더 많은 편집 가능성을 제공합니다.",
            "화각": "렌즈가 담아낼 수 있는 장면의 범위를 의미합니다. 광각렌즈는 넓은 화각을, 망원렌즈는 좁은 화각을 가집니다.",
            "초점거리": "렌즈의 광학적 중심에서 이미지 센서까지의 거리를 밀리미터(mm) 단위로 나타낸 값입니다. 화각과 배율을 결정하는 중요한 요소입니다.",
        }
        
        # 테스트 유저를 위한 초기 세션 생성
        test_user_id = 12345
        test_session = {
            "sessionId": 1,
            "userId": test_user_id,
            "title": "카메라 상담 테스트",
            "createdAt": "2024-03-20T10:00:00",
            "updatedAt": "2024-03-20T10:00:00"
        }
        
        # 테스트 세션 저장
        self.sessions[test_user_id] = [test_session]
        
        # 테스트 메시지 저장
        self.chat_messages[1] = [{
            "messageId": 1,
            "userMessage": "카메라 추천해주세요",
            "aiMessage": "이 메세지는 테스트 용으로 저장되었습니다.",
            "keywords": ["카메라", "DSLR", "미러리스"],
            "suggestedQuestions": [
                "추천 질문 1입니다.",
                "전문가용 카메라는 어떤 것이 있나요?",
                "입문자용 카메라를 추천해주세요"
            ]
        }]
        
    def _hash_password(self, password: str) -> str:
        """간단한 비밀번호 해싱 (실제 서비스에서는 더 안전한 방식 사용)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str) -> dict:
        """새 사용자 생성"""
        if email in self.users:
            return {"success": False, "message": "이미 가입된 사용자입니다."}
        
        # 새 사용자 ID 생성 (실제로는 더 안전한 방식 사용)
        new_user_id = max([user["userId"] for user in self.users.values()], default=0) + 1
        
        user_data = {
            "username": username,
            "password": self._hash_password(password),
            "email": email,
            "userId": new_user_id,
            "created_at": datetime.now().isoformat()
        }
        
        self.users[email] = user_data
        return {"success": True, "message": "가입성공"}

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """사용자 ID로 사용자 찾기"""
        for user in self.users.values():
            if user["userId"] == user_id:
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """이메일로 사용자 찾기"""
        return self.users.get(email)

    def verify_user(self, email: str, password: str) -> dict:
        """사용자 로그인 검증"""
        user = self.users.get(email)
        if not user:
            return {"success": False, "message": "이메일 또는 비밀번호가 일치하지 않습니다."}
        
        if user["password"] != self._hash_password(password):
            return {"success": False, "message": "이메일 또는 비밀번호가 일치하지 않습니다."}
        
        return {
            "success": True,
            "userId": user["userId"],
            "username": user["username"],
            "email": user["email"]
        }
    
    def add_user(self, username: str, user_data: dict) -> bool:
        if username in self.users:
            return False
        self.users[username] = user_data
        return True
    
    def get_user_by_username(self, username: str) -> dict:
        return self.users.get(username)
    
    def get_user_by_email(self, email: str) -> dict:
        return next(
            (user for user in self.users.values() if user["email"] == email),
            None
        )

    def get_user_sessions(self, user_id: int) -> List[dict]:
        """사용자의 모든 세션 조회"""
        sessions = self.sessions.get(user_id, [])
        print(f"[DB] Retrieved {len(sessions)} sessions for user {user_id}")
        for session in sessions:
            print(f"[DB] Session {session['sessionId']}: {session['title']}")
        return sorted(
            sessions,
            key=lambda x: x['updatedAt'],
            reverse=True
        )

    def create_session(self, user_id: int, session_data: dict):
        """새로운 세션 생성"""
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        self.sessions[user_id].append(session_data)
    
    def create_dummy_session(self, user_id: int):
        """테스트용 더미 세션 생성 (최초 1회만)"""
        existing_sessions = self.get_user_sessions(user_id)
        if existing_sessions:
            return  # 이미 세션이 있으면 생성하지 않음
            
        title = f"카메라 상담 {datetime.now().strftime('%Y-%m-%d')}"
        session_id = self.create_new_session(user_id, title)
        
        # 더미 메시지 생성
        dummy_messages = [
            {
                "messageId": self.current_message_id + 1,
                "userMessage": "카메라 추천해주세요",
                "aiMessage": "어떤 용도로 카메라를 사용하실 계획이신가요? 주로 여행용, 전문 촬영용 등 사용 목적에 따라 추천드릴 수 있습니다.",
                "keywords": ["카메라", "DSLR", "미러리스"],
                "suggestedQuestions": [
                    "여행용 카메라를 찾고 있어요",
                    "전문가용 카메라는 어떤 것이 있나요?",
                    "입문자용 카메라를 추천해주세요"
                ]
            }
        ]
        self.chat_messages[session_id] = dummy_messages
        self.current_message_id += 1

    def get_chat_history(self, session_id: int) -> list:
        """세션의 채팅 기록 조회"""
        return self.chat_messages.get(session_id, [])
    
    def create_dummy_chat_history(self, session_id: int):
        """카메라 관련 더미 채팅 기록 생성"""
        dummy_messages = [
            {
                "messageId": 1,
                "userMessage": "카메라 입문자인데 어떤 카메라를 사면 좋을까요?",
                "aiMessage": "카메라 입문자라면 미러리스 카메라를 추천드립니다. DSLR에 비해 크기가 작고 가벼우며, 최근에는 성능도 매우 우수합니다...",
                "keywords": ["DSLR", "미러리스"],
                "suggestedQuestions": [
                    "미러리스 카메라의 장점이 궁금합니다",
                    "입문용 카메라의 가격대는 어떻게 되나요?",
                    "렌즈는 어떤 것을 선택해야 할까요?"
                ]
            },
            {
                "messageId": 2,
                "userMessage": "조리개와 셔터스피드는 어떤 관계가 있나요?",
                "aiMessage": "조리개와 셔터스피드는 모두 카메라에 들어오는 빛의 양을 조절하는 요소입니다. 조리개는 한 번에 들어오는 빛의 양을, 셔터스피드는 빛이 들어오는 시간을 조절합니다...",
                "keywords": ["조리개", "셔터스피드"],
                "suggestedQuestions": [
                    "적정 노출을 맞추는 방법이 궁금합니다",
                    "조리개 우선 모드는 언제 사용하나요?",
                    "셔터스피드 우선 모드의 장점은 무엇인가요?"
                ]
            }
        ]
        self.chat_messages[session_id] = dummy_messages

    def create_new_session(self, user_id: int, title: str) -> int:
        """새 세션 생성"""
        self.current_session_id += 1
        self._current_session_id = self.current_session_id  # 임시 저장
        
        if user_id not in self.sessions:
            self.sessions[user_id] = []
            
        session = {
            "sessionId": self.current_session_id,
            "userId": user_id,
            "title": title,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        self.sessions[user_id].append(session)
        self.chat_messages[self.current_session_id] = []  # 빈 메시지 배열로 초기화
        return self.current_session_id
    
    def add_message_to_session(self, session_id: int, user_message: str, ai_message: str,
                             keywords: List[str], suggested_questions: List[str]) -> dict:
        """세션에 새 메시지 추가"""
        if session_id not in self.chat_messages:
            print(f"[DB] Creating new message array for session {session_id}")
            self.chat_messages[session_id] = []

        self.current_message_id += 1
        message = {
            "messageId": self.current_message_id,
            "userMessage": user_message,
            "aiMessage": ai_message,
            "keywords": keywords,
            "suggestedQuestions": suggested_questions
        }
        
        self.chat_messages[session_id].append(message)
        
        # 세션의 updatedAt 시간 업데이트
        for user_sessions in self.sessions.values():
            for session in user_sessions:
                if session["sessionId"] == session_id:
                    session["updatedAt"] = datetime.now().isoformat()
                    break
        
        print(f"[DB] Added message to session {session_id}: {message}")
        return message

    def get_session_messages(self, session_id: int) -> List[dict]:
        """세션의 모든 메시지 조회"""
        messages = self.chat_messages.get(session_id, [])
        print(f"[DB] Retrieved {len(messages)} messages for session {session_id}")
        for msg in messages:
            print(f"[DB] Message {msg['messageId']}: {msg['userMessage'][:50]}...")
        return messages

    async def generate_chat_response(self, question: str, session_id: int = None, brand: str = None, model: str = None):
        """채팅 응답 생성 (스트리밍용)"""
        # 현재 세션 ID 저장
        self._current_session_id = session_id
        print(f"[DB] Generating response for session {self._current_session_id}")

        # 초기 생각하는 상태
        yield {
            "currentNode": "thinking",
            "answer": "",
            "keywords": [],
            "suggestedQuestions": []
        }

        await asyncio.sleep(1)  # 생각하는 시간 시뮬레이션

        # 답변 시작
        base_response = "어떤 용도로 카메라를 사용하실 계획이신가요? "
        chunks = [
            "어떤 ", "용도로 ", "카메라를 ", "사용하실 ", "계획이신가요? ",
            "주로 ", "여행용, ", "전문 ", "촬영용 ", "등 ",
            "사용 ", "목적에 ", "따라 ", "추천드릴 ", "수 ", "있습니다."
        ]

        accumulated_answer = ""
        for chunk in chunks:
            accumulated_answer += chunk
            yield {
                "currentNode": "generate",
                "answer": chunk,
                "keywords": [],
                "suggestedQuestions": []
            }
            await asyncio.sleep(0.2)  # 각 청크 사이 딜레이

        # 최종 응답
        keywords = ["카메라", "DSLR", "미러리스"]
        suggested_questions = [
            "여행용 카메라를 찾고 있어요",
            "전문가용 카메라는 어떤 것이 있나요?",
            "입문자용 카메라를 추천해주세요"
        ]

        # 내부적으로 메시지 저장 (세션 ID 확인)
        if self._current_session_id:
            print(f"[DB] Saving message to session {self._current_session_id}")
            self.add_message_to_session(
                self._current_session_id,
                question,
                accumulated_answer,
                keywords,
                suggested_questions
            )
        else:
            print("[DB] Warning: No session ID available for message storage")

        # 기존 응답 형식 유지
        yield {
            "currentNode": "complete",
            "answer": accumulated_answer,
            "keywords": keywords,
            "suggestedQuestions": suggested_questions
        }

# Global database instance
db = MockDB() 