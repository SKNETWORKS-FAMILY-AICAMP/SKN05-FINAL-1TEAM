from datetime import datetime
from typing import Dict, List, Optional
import random
import jwt
import hashlib

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
        self.sessions: Dict[int, dict] = {}  # 세션 저장소
        self.chat_messages: Dict[int, List[dict]] = {}  # 채팅 메시지 저장소
        self.current_session_id = 0
        self.current_message_id = 0
        self.keywords_db = {
            "Python워크": "소프트웨어 개발을 위한 기본 구조와 도구들을 제공하는 플랫폼입니다. 개발자가 핵심 기능 구현에 집중할 수 있도록 도와줍니다.",
            "DSLR": "Digital Single-Lens Reflex의 약자로, 디지털 일안 반사식 카메라입니다. 렌즈를 통해 들어온 빛이 반사거울에 반사되어 뷰파인더로 전달되는 방식의 카메라입니다.",
            "미러리스": "반사거울이 없는 디지털 카메라로, DSLR보다 작고 가벼운 것이 특징입니다. 최근에는 성능면에서도 DSLR과 대등하거나 뛰어난 제품들이 많습니다.",
            "조리개": "카메라 렌즈에서 빛이 통과하는 구멍의 크기를 조절하는 장치입니다. F값으로 표시되며, 피사계 심도와 밝기를 조절하는 중요한 요소입니다.",
            "셔터스피드": "카메라의 셔터가 열려있는 시간을 의미합니다. 빠른 셔터스피드는 움직이는 피사체를 선명하게 촬영할 수 있고, 느린 셔터스피드는 움직임을 표현할 수 있습니다.",
            "ISO": "이미지 센서의 빛 감도를 나타내는 수치입니다. 높은 ISO는 어두운 환경에서 촬영이 가능하지만, 노이즈가 증가할 수 있습니다.",
            "RAW": "카메라 센서가 캡처한 모든 이미지 데이터를 포함하는 파일 형식입니다. JPEG보다 더 많은 편집 가능성을 제공합니다.",
            "화각": "렌즈가 담아낼 수 있는 장면의 범위를 의미합니다. 광각렌즈는 넓은 화각을, 망원렌즈는 좁은 화각을 가집니다.",
            "초점거리": "렌즈의 광학적 중심에서 이미지 센서까지의 거리를 밀리미터(mm) 단위로 나타낸 값입니다. 화각과 배율을 결정하는 중요한 요소입니다."
        }
        
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

    def get_user_sessions(self, user_id: int) -> list:
        """사용자의 세션 목록 조회"""
        user_sessions = []
        for session_id, session in self.sessions.items():
            if int(session["userId"]) == user_id:
                user_sessions.append({
                    "sessionId": session_id,
                    "title": session["title"],
                    "createdAt": session["createdAt"],
                    "updatedAt": session["updatedAt"]
                })
        return sorted(user_sessions, key=lambda x: x["createdAt"], reverse=True)

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
                "suggestQuestions": [
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
                "suggestQuestions": [
                    "적정 노출을 맞추는 방법이 궁금합니다",
                    "조리개 우선 모드는 언제 사용하나요?",
                    "셔터스피드 우선 모드의 장점은 무엇인가요?"
                ]
            }
        ]
        self.chat_messages[session_id] = dummy_messages

    def create_new_session(self, user_id: int, title: str) -> int:
        """새로운 세션 생성"""
        self.current_session_id += 1
        current_time = datetime.now().isoformat()
        session = {
            "sessionId": self.current_session_id,
            "userId": user_id,
            "title": title,
            "createdAt": current_time,
            "updatedAt": current_time
        }
        self.sessions[self.current_session_id] = session
        return self.current_session_id
    
    def create_message(self, session_id: int, question: str, llm_response: dict) -> int:
        """새로운 메시지 생성"""
        self.current_message_id += 1
        message = {
            "messageId": self.current_message_id,
            "userMessage": question,
            "aiMessage": llm_response["answer"],
            "keywords": llm_response["keywords"],
            "suggestedQuestions": llm_response["suggestQuestions"]
        }
        
        if session_id not in self.chat_messages:
            self.chat_messages[session_id] = []
        
        self.chat_messages[session_id].append(message)
        
        # 세션 업데이트 시간 갱신
        if session_id in self.sessions:
            self.sessions[session_id]["updatedAt"] = datetime.now().isoformat()
            
        return self.current_message_id
    
    def mock_llm_response(self, question: str, brand: str = None, model: str = None) -> dict:
        """카메라 관련 LLM 응답을 모사하는 메서드"""
        responses = [
            {
                "currentNode": "camera_basic",
                "answer": f"카메라에 대해 답변드리겠습니다. " + 
                         (f"\n{brand} 브랜드의 " if brand else "") +
                         (f"{model} 모델의 경우, " if model else "") +
                         f"\n\n{question}에 대해 설명드리자면, 카메라의 기본 원리는 빛을 통해 이미지를 기록하는 것입니다. 현대의 디지털 카메라는 이미지 센서를 통해 빛을 전기 신호로 변환하여 이미지를 저장합니다...",
                "keywords": ["DSLR", "미러리스", "디지털카메라"],
                "suggestQuestions": [
                    "카메라의 기본 설정은 어떻게 하나요?",
                    "좋은 사진을 찍기 위한 팁이 있을까요?",
                    "카메라 종류별 장단점이 궁금합니다."
                ]
            },
            {
                "currentNode": "camera_technical",
                "answer": f"기술적인 측면에서 설명드리겠습니다. " +
                         (f"\n{brand} " if brand else "") +
                         (f"{model}의 경우, " if model else "") +
                         f"\n\n{question}에 대해, 카메라의 노출은 조리개, 셔터스피드, ISO의 세 가지 요소로 결정됩니다...",
                "keywords": ["조리개", "셔터스피드", "ISO"],
                "suggestQuestions": [
                    "조리개 값은 어떻게 설정하는 것이 좋나요?",
                    "야간 촬영시 주의할 점은 무엇인가요?",
                    "삼각대는 언제 사용하면 좋을까요?"
                ]
            },
            {
                "currentNode": "camera_advanced",
                "answer": f"고급 촬영 기법에 대해 설명드리겠습니다. " +
                         (f"\n{brand} " if brand else "") +
                         (f"{model} 카메라로 " if model else "") +
                         f"\n\n{question}에 대해, RAW 촬영과 후보정을 통해 더 좋은 결과물을 얻을 수 있습니다...",
                "keywords": ["RAW", "화각", "초점거리"],
                "suggestQuestions": [
                    "RAW 파일의 장점은 무엇인가요?",
                    "렌즈 선택은 어떻게 하면 좋을까요?",
                    "포트레이트 촬영 팁을 알려주세요."
                ]
            }
        ]
        return random.choice(responses)

# Global database instance
db = MockDB() 