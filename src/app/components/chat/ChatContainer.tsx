'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import styles from '@/app/styles/chat.module.css';
import { ChatInput } from './ChatInput';
import { UserMessage } from './UserMessage';
import { AIMessage } from './AIMessage';
import { useUserStore } from '@/app/store/userStore';
import { useBrandStore } from '@/app/store/brandStore';

interface Message {
  messageId: number;
  userMessage: string;
  aiMessage: string;
  keywords: string[];
  suggestedQuestions: string[];
}

export function ChatContainer() {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { userId, accessToken } = useUserStore();
  const { selectedBrand, selectedModel } = useBrandStore();
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [currentAnswer, setCurrentAnswer] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);

  // 스크롤을 맨 아래로 이동시키는 함수
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // messages가 업데이트될 때마다 스크롤 이동
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 세션 히스토리 불러오기
  const loadSessionHistory = useCallback(async (sessionId: number) => {
    if (!userId || !accessToken) return;

    setIsLoading(true);
    try {
      console.log('Loading history for session:', sessionId); // 디버깅용
      const response = await fetch(
        `http://localhost:8000/api/chat/history?userId=${userId}&sessionId=${sessionId}`,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          }
        }
      );

      if (!response.ok) {
        throw new Error('Failed to load session history');
      }

      const data = await response.json();
      if (data.Messages && Array.isArray(data.Messages)) {
        console.log('Received messages:', data.Messages); // 디버깅용
        setMessages(data.Messages);
        setCurrentSessionId(sessionId);
      } else {
        console.error('Invalid message format:', data); // 디버깅용
      }
    } catch (error) {
      console.error('Error loading session history:', error);
    } finally {
      setIsLoading(false);
    }
  }, [userId, accessToken]);

  // 세션 선택 이벤트 리스너
  useEffect(() => {
    const handleSessionSelected = (event: CustomEvent<number>) => {
      console.log('Session selected:', event.detail); // 디버깅용
      loadSessionHistory(event.detail);
    };

    window.addEventListener('sessionSelected', handleSessionSelected as EventListener);

    return () => {
      window.removeEventListener('sessionSelected', handleSessionSelected as EventListener);
    };
  }, [userId, accessToken, loadSessionHistory]); // loadSessionHistory 의존성 추가

  // 새 대화 시작 이벤트 리스너
  useEffect(() => {
    const handleNewChat = () => {
      setCurrentSessionId(null);
      setMessages([]);
    };

    window.addEventListener('startNewChat', handleNewChat);

    return () => {
      window.removeEventListener('startNewChat', handleNewChat);
    };
  }, []);

  const handleSendMessage = async (message: string) => {
    if (!userId || isLoading) return;

    setIsLoading(true);
    setIsGenerating(true);
    setCurrentAnswer("");
    
    // 사용자 메시지를 즉시 추가
    const userMessageId = Date.now();
    setMessages(prev => [...prev, {
      messageId: userMessageId,
      userMessage: message,
      aiMessage: "",  // AI 답변은 아직 없음
      keywords: [],
      suggestedQuestions: []
    }]);
    
    try {
      const response = await fetch('http://localhost:8000/api/chat/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
          userId: userId,
          sessionId: currentSessionId,
          brand: selectedBrand || null,
          model: selectedModel || null
        }),
      });

      const reader = response.body!.getReader();
      let accumulatedAnswer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        // 청크를 문자열로 변환
        const chunk = new TextDecoder().decode(value);
        const lines = chunk.split('\n').filter(line => line.trim());

        for (const line of lines) {
          const data = JSON.parse(line);
          
          if (data.currentNode === "thinking") {
            setCurrentAnswer("답변을 생성하는 중...");
          } 
          else if (data.currentNode === "generate") {
            accumulatedAnswer += data.answer;
            setCurrentAnswer(accumulatedAnswer);
          }
          else if (data.currentNode === "complete") {
            // 새 세션이 생성된 경우
            if (!currentSessionId && data.sessionId) {
              setCurrentSessionId(data.sessionId);
              console.log('Creating new session with ID:', data.sessionId); // 디버깅용
              // 새 세션 생성 이벤트 발생
              const event = new CustomEvent('sessionCreated', {
                detail: { sessionId: data.sessionId }
              });
              window.dispatchEvent(event);
            }

            // 기존 메시지 배열에서 사용자 메시지는 유지하고 AI 답변만 업데이트
            setMessages(prev => prev.map(msg => 
              msg.messageId === userMessageId
                ? {
                    ...msg,
                    aiMessage: accumulatedAnswer,
                    keywords: data.keywords,
                    suggestedQuestions: data.suggestedQuestions
                  }
                : msg
            ));
            setCurrentAnswer("");
            setIsGenerating(false);
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setCurrentAnswer("오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeywordClick = (keyword: string) => {
    // KeywordDescriptionContainer의 fetchKeywordDescription 호출
    // 이벤트를 발생시켜 사이드바의 KeywordDescriptionContainer에 알림
    const event = new CustomEvent('keywordSelected', { detail: keyword });
    window.dispatchEvent(event);
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messagesContainer}>
        <div className={styles.messagesWrapper}>
          {messages.map((message: Message) => (
            <div key={message.messageId} className={styles.messageGroup}>
              <UserMessage message={message.userMessage} />
              {message.aiMessage ? (
                <AIMessage 
                  message={message.aiMessage}
                  keywords={message.keywords}
                  suggestedQuestions={message.suggestedQuestions}
                  onQuestionClick={handleSendMessage}
                  onKeywordClick={handleKeywordClick}
                />
              ) : (
                <AIMessage 
                  message={currentAnswer}
                  keywords={[]}
                  suggestedQuestions={[]}
                  onQuestionClick={handleSendMessage}
                  onKeywordClick={handleKeywordClick}
                  isGenerating={isGenerating}
                />
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
