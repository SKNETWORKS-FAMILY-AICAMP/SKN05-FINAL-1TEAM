import { create } from 'zustand';

// 세션 내 메시지들 타입
export interface Message {
  messageId: string;
  userMessage: string;    // 사용자 메시지
  aiMessage: string;      // AI 응답 메시지
  keywords: string[];     // 추출된 키워드 목록
  suggestedQuestions: string[]; // 추천 질문 목록
  createdAt: string;
}

// 채팅 세션 타입
export interface ChatSession {
  sessionId: string;
  userId: string;
  title: string;
  messages: Message[];
  createdAt: string;
  updatedAt: string;
}

// 메시지 스토어 인터페이스
interface MessageStore {
  currentSession: ChatSession | null; // 현재 세션
  sessions: ChatSession[]; // 세션 목록
  setCurrentSession: (session: ChatSession) => void; // 현재 세션 설정
  addMessage: (message: Message) => void; // 메시지 추가
  setSessions: (sessions: ChatSession[]) => void; // 세션 목록 설정
  clearCurrentSession: () => void; // 현재 세션 초기화
}

// 메시지 스토어 생성
export const useMessageStore = create<MessageStore>((set) => ({
  currentSession: null, // 현재 세션
  sessions: [], // 세션 목록
  setCurrentSession: (session) => set({ currentSession: session }), // 현재 세션 설정
  addMessage: (message) => set((state) => ({
    currentSession: state.currentSession ? {
      ...state.currentSession,
      messages: [...state.currentSession.messages, message],
      updatedAt: new Date().toISOString()
    } : null
  })),
  setSessions: (sessions) => set({ sessions }),
  clearCurrentSession: () => set({ currentSession: null })
}));