'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import styles from '@/app/styles/chat.module.css';
import { ChatInput } from './ChatInput';
import { UserMessage } from './UserMessage';
import { AIMessage } from './AIMessage';
import { CurrentNodeMessage } from './CurrentNodeMessage';
import { useUserStore } from '@/app/store/userStore';
import { useBrandStore } from '@/app/store/brandStore';


interface Message {
  message_id: number;
  userMessage: string;
  aiMessage: string;
  keywords: string[];
  suggestQuestions: string[];
}

interface Session {
  session_id: number;
  title: string;
  updated_date: string;
  create_date: string;
}

export function ChatContainer() {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { accessToken } = useUserStore();
  const { selectedBrand, selectedModel } = useBrandStore();
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [currentAnswer, setCurrentAnswer] = useState<string>("");
  const [currentNodes, setCurrentNodes] = useState<{ message_id: number; currentNodes: string[]; }>({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [isReverseQ, setIsReverseQ] = useState(false);
  const keywordsRef = useRef([]);
  const suggestQuestionsRef = useRef([]);

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
    if (!accessToken) return;

    setIsLoading(true);
    try {
      console.log('Loading history for session:', sessionId); // 디버깅용
      const response = await fetch(
        `http://localhost:8000/api/chat/history?session_id=${sessionId}`,
        {
          headers: {
              'Authorization': `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
          }
        }
      );

      if (!response.ok) {
        throw new Error('Failed to load session history');
      }

      const data = await response.json();
      if (data.Messages && Array.isArray(data.Messages)) {
        console.log('Received messages:', data.Messages); // 디버깅용
        setMessages(data.Messages.map((msg: any) => ({
            message_id: msg.message_id,
            userMessage: msg.userMessage,
            aiMessage: msg.aiMessage,
            keywords: msg.keywords || [],
            suggestQuestions: msg.suggestQuestions || []  // suggestQuestions로 변경
          })));
        setCurrentSessionId(sessionId);
      } else {
        console.error('Invalid message format:', data); // 디버깅용
      }
    } catch (error) {
      console.error('Error loading session history:', error);
    } finally {
      setIsLoading(false);
    }
  }, [accessToken]);

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
  }, [accessToken, loadSessionHistory]); // loadSessionHistory 의존성 추가

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
    if (!accessToken || isLoading) return;

    setIsLoading(true);
    setIsGenerating(true);
    setCurrentAnswer("");
    setIsReverseQ(false);
    
    // 사용자 메시지를 즉시 추가
    const userMessageId = Date.now();
    setMessages(prev => [...prev, {
      message_id: userMessageId,
      userMessage: message,
      aiMessage: "",  // AI 답변은 아직 없음
      keywords: [],
      suggestQuestions: []
    }]);
    
    // 요청 데이터 준비 및 검증
    const requestData = {
      question: message,
      session_id: currentSessionId || undefined,  // undefined로 변경
      brand: selectedBrand || "",
      model: selectedModel || ""
    };
    
    // undefined 필드 제거
    const cleanRequestData = Object.fromEntries(
      Object.entries(requestData).filter(([_, value]) => value !== undefined)
    );
    
    console.log('Clean request data:', cleanRequestData); // 디버깅용
    
    try {
      let response;

      if (!isReverseQ) {
        response = await fetch('http://localhost:8000/api/chat/answer', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          },
          body: JSON.stringify(cleanRequestData),
        });
      }

      else if (isReverseQ) {
        response = await fetch('http://localhost:8000/api/chat/rqanswer', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          },
          body: JSON.stringify(cleanRequestData),
        });
        setIsReverseQ(false)
        keywordsRef.current = [];
        suggestQuestionsRef.current = [];
      }

        if (!response.ok) {
          const errorData = await response.json();
          console.error('Error details:', {
            status: response.status,
            statusText: response.statusText,
            error: errorData
          });
          throw new Error(`Request failed: ${JSON.stringify(errorData)}`);
        }

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let accumulatedAnswer = "";
      let accumulatedNode = {
        message_id: 0,
        currentNodes: []
      }
      let buffer = ""; // 불완전한 청크를 저장하기 위한 버퍼
      
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        // 새로운 청크를 버퍼에 추가
        buffer += decoder.decode(value, { stream: true });
        
        // 완전한 줄들을 처리
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // 마지막 불완전한 줄을 버퍼에 저장

        for (const line of lines) {
          if (line.trim() === '') continue;
          
          try {
            const data = JSON.parse(line);

            if (!currentSessionId && data.sessionId) {
              setCurrentSessionId(data.sessionId);
              console.log('Creating new session with ID:', data.sessionId);
              const event = new CustomEvent('sessionCreated', {
                detail: { sessionId: data.sessionId }
              });
              window.dispatchEvent(event);
            }

            if (data.currentNode === "refine_question") {
              setIsReverseQ(true)

              accumulatedAnswer += data.answer;
              setCurrentAnswer(accumulatedAnswer);

              accumulatedNode.currentNodes.push("END")
              setCurrentNodes({
                ...accumulatedNode, // ✅ 기존 객체 복사 → 새로운 객체 생성
                message_id: userMessageId, // ✅ 새로운 message_id 값 할당
                currentNodes: [...accumulatedNode.currentNodes], // ✅ 기존 배열을 복사하고 새로운 값 추가
              });

              // 기존 메시지 배열에서 사용자 메시지는 유지하고 AI 답변만 업데이트
              setMessages(prev => prev.map(msg => 
                msg.message_id === userMessageId
                  ? {
                      ...msg,
                      aiMessage: accumulatedAnswer,
                      keywords: data.keywords,
                      suggestQuestions: data.suggestQuestions
                    }
                  : msg
              ));
              setCurrentAnswer("");
              setIsGenerating(false);
            }

            else if (data.currentNode === "not_for_camera") {
              accumulatedAnswer += data.answer;
              setCurrentAnswer(accumulatedAnswer);

              accumulatedNode.currentNodes.push("END")
              setCurrentNodes({
                ...accumulatedNode, // ✅ 기존 객체 복사 → 새로운 객체 생성
                message_id: userMessageId, // ✅ 새로운 message_id 값 할당
                currentNodes: [...accumulatedNode.currentNodes], // ✅ 기존 배열을 복사하고 새로운 값 추가
              });

              // 기존 메시지 배열에서 사용자 메시지는 유지하고 AI 답변만 업데이트
              setMessages(prev => prev.map(msg => 
                msg.message_id === userMessageId
                  ? {
                      ...msg,
                      aiMessage: accumulatedAnswer,
                      keywords: data.keywords,
                      suggestQuestions: data.suggestQuestions
                    }
                  : msg
              ));
              setCurrentAnswer("");
              setIsReverseQ(false)
              setIsGenerating(false);
            } 

            else if (data.currentNode === "답변 생성 중") {
              accumulatedAnswer += data.answer;
              setCurrentAnswer(accumulatedAnswer);
              
              // 현재 노드가 이전 노드와 같지 않다면 진행중인 노드 배열에 추가
              if (accumulatedNode.currentNodes.at(-1) !== data.currentNode) {
                accumulatedNode.currentNodes.push(data.currentNode);
                setCurrentNodes({
                  ...accumulatedNode, // ✅ 기존 객체 복사 → 새로운 객체 생성
                  message_id: userMessageId, // ✅ 새로운 message_id 값 할당
                  currentNodes: [...accumulatedNode.currentNodes] // ✅ 기존 배열을 복사하고 새로운 값 추가
                });
              }
            }

            else {
              if (accumulatedNode.currentNodes.at(-1) !== data.currentNode) {
                accumulatedNode.currentNodes.push(data.currentNode);
                setCurrentNodes({
                  ...accumulatedNode, // ✅ 기존 객체 복사 → 새로운 객체 생성
                  message_id: userMessageId, // ✅ 새로운 message_id 값 할당
                  currentNodes: [...accumulatedNode.currentNodes] // ✅ 기존 배열을 복사하고 새로운 값 추가
                });
              }

              if (Array.isArray(data.keywords) && data.keywords.length > 0) {
                keywordsRef.current = data.keywords;
              }
              if (Array.isArray(data.suggestQuestions) && data.suggestQuestions.length > 0) {
                suggestQuestionsRef.current = data.suggestQuestions;
              }

              if (
                keywordsRef.current.length > 0 &&
                suggestQuestionsRef.current.length > 0
              ) {
                  setCurrentNodes({
                    message_id: userMessageId,
                    currentNodes: ["END"]
                  })
                  
                  setMessages(prev =>
                    prev.map(msg =>
                      msg.message_id === userMessageId
                        ? {
                            ...msg,
                            aiMessage: accumulatedAnswer,
                            keywords: [...keywordsRef.current], // 최신 리스트 복사
                            suggestQuestions: [...suggestQuestionsRef.current] // 최신 리스트 복사
                          }
                        : msg
                    )
                  );
                  setCurrentAnswer("");
                  setIsGenerating(false);
              }
            }
          } catch (error) {
            console.error('Error parsing line:', line, error);
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
            <div key={message.message_id} className={styles.messageGroup}>
              <UserMessage message={message.userMessage} />
                {message.message_id == currentNodes.message_id && (
                    <CurrentNodeMessage currentNodes={currentNodes.currentNodes} />
                )}

              {message.aiMessage ? (
                <AIMessage 
                  message={message.aiMessage}
                  keywords={message.keywords}
                  suggestedQuestions={message.suggestQuestions}
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