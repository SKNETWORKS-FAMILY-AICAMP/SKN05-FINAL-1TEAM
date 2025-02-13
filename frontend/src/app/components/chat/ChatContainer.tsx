'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import styles from '@/app/styles/chat.module.css';
import { ChatInput } from './ChatInput';
import { UserMessage } from './UserMessage';
import { AIMessage } from './AIMessage';
import { ProgressStep } from './ProgressSteps';
import { useUserStore } from '@/app/store/userStore';
import { useBrandStore } from '@/app/store/brandStore';


interface Message {
  message_id: number;
  userMessage: string;
  aiMessage: string;
  keywords: string[];
  suggestQuestions: string[];
}

// current Node 내용
interface NodeState {
  message_id: number;
  currentNodes: string[];
}


interface ChatState {
  messages: Message[];
  currentAnswer: string;
  currentNodes: NodeState;
  isGenerating: boolean;
  isReverseQ: boolean;
  currentSessionId: number | null;
}

export function ChatContainer() {
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const keywordsRef = useRef([]);
  const suggestQuestionsRef = useRef([]);

  // Store hooks
  const { accessToken } = useUserStore();
  const { selectedBrand, selectedModel } = useBrandStore();

  // state
  const [state, setState] = useState<ChatState>({
    messages: [],
    currentAnswer: "",
    currentNodes: { message_id: 0, currentNodes: [] },
    isGenerating: false,
    isReverseQ: false,
    currentSessionId: null
  });
  const [isLoading, setIsLoading] = useState(false);

  // 상태 업테이트 헬퍼
  const updateState = (updates: Partial<ChatState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }

  // 자동 스크롤
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [state.messages]);

  // 세션 히스토리 로드
  const loadSessionHistory = useCallback(async (sessionId: number) => {
    if (!accessToken) return;

    setIsLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/chat/history?session_id=${sessionId}`,
        {
          headers: {
              'Authorization': `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
          }
        }
      );

      if (!response.ok) throw new Error('Failed to load session history');

      const data = await response.json();
      if (data.Messages && Array.isArray(data.Messages)) {
        updateState({
            messages: data.Messages.map((msg: any) => ({
                message_id: msg.message_id,
                userMessage: msg.userMessage,
                aiMessage: msg.aiMessage,
                keywords: msg.keywords || [],
                suggestQuestions: msg.suggestQuestions || []  // suggestQuestions로 변경
          })),
          currentSessionId: sessionId
        });
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
        updateState({
            currentSessionId: null,
            messages: []
        });
    };

    window.addEventListener('startNewChat', handleNewChat);

    return () => {
      window.removeEventListener('startNewChat', handleNewChat);
    };
  }, []);

  // 스트림 응답 처리
  const handleStreamResponse = async (reader: ReadableStreamDefaultReader<Uint8Array>, decoder: TextDecoder, userMessageId: number) => {
    let accumulatedAnswer = "";
    let accumulatedNode = { message_id: 0, currentNodes: [] };
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.trim()) continue;
        
        try {
          const data = JSON.parse(line);
          handleStreamData(data, userMessageId, accumulatedAnswer, accumulatedNode);
        } catch (error) {
          console.error('Error parsing line:', line, error);
        }
      }
    }
  };

  // 스트림 데이터 처리
  const handleStreamData = (
    data: any, 
    userMessageId: number, 
    accumulatedAnswer: string, 
    accumulatedNode: NodeState
  ) => {
    // 세션 ID 처리
    if (!state.currentSessionId && data.sessionId) {
      updateState({ currentSessionId: data.sessionId });
      window.dispatchEvent(new CustomEvent('sessionCreated', {
        detail: { sessionId: data.sessionId }
      }));
    }

    // 노드 상태 업데이트
    if (accumulatedNode.currentNodes.at(-1) !== data.currentNode) {
      accumulatedNode.currentNodes.push(data.currentNode);
      updateState({
        currentNodes: {
          message_id: userMessageId,
          currentNodes: [...accumulatedNode.currentNodes]
        }
      });
    }

    // 답변 누적
    accumulatedAnswer += data.answer || "";
    updateState({ currentAnswer: accumulatedAnswer });

    // 키워드와 제안 질문 처리
    if (Array.isArray(data.keywords)) keywordsRef.current = data.keywords;
    if (Array.isArray(data.suggestQuestions)) suggestQuestionsRef.current = data.suggestQuestions;

    // 메시지 완료 처리
    if (data.currentNode === "END" || 
        (keywordsRef.current.length > 0 && suggestQuestionsRef.current.length > 0)) {
      finishMessage(userMessageId, accumulatedAnswer);
    }
  };  

  // 메시지 완료 처리
  const finishMessage = (userMessageId: number, finalAnswer: string) => {
    updateState({
      messages: state.messages.map(msg =>
        msg.message_id === userMessageId
          ? {
              ...msg,
              aiMessage: finalAnswer,
              keywords: [...keywordsRef.current],
              suggestQuestions: [...suggestQuestionsRef.current]
            }
          : msg
      ),
      currentAnswer: "",
      currentNodes: { message_id: userMessageId, currentNodes: ["END"] },
      isGenerating: false
    });
  };

  const handleSendMessage = async (message: string) => {
    if (!accessToken || state.isLoading) return;

    const userMessageId = Date.now();
    updateState({
      isGenerating: true,
      currentAnswer: "",
      isReverseQ: false,
      messages: [...state.messages, {
        message_id: userMessageId,
        userMessage: message,
        aiMessage: "",
        keywords: [],
        suggestQuestions: []
      }]
    });
    setIsLoading(true);
    
    try {
        const response = await fetch(
            `http://localhost:8000/api/chat/${state.isReverseQ ? 'rqanswer' : 'answer'}`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
              },
              body: JSON.stringify({
                question: message,
                session_id: state.currentSessionId,
                brand: selectedBrand,
                model: selectedModel
              })
            }
          );

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
        await handleStreamResponse(reader, decoder, userMessageId)
    } catch (error) {
      console.error('Error sending message:', error);
      updateState({ currentAnswer: "오류가 발생했습니다." });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeywordClick = (keyword: string) => {
      // 이벤트를 발생시켜 사이드바의 KeywordDescriptionContainer에 알림
    window.dispatchEvent(new CustomEvent('keywordSelected', { detail: keyword }));
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messagesContainer}>
        <div className={styles.messagesWrapper}>
          {state.messages.map((message: Message) => (
            <div key={message.message_id} className={styles.messageGroup}>
              <UserMessage message={message.userMessage} />
                {message.message_id == state.currentNodes.message_id && (
                    <ProgressStep currentNodes={state.currentNodes.currentNodes} />
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
                  message={state.currentAnswer}
                  keywords={[]}
                  suggestedQuestions={[]}
                  onQuestionClick={handleSendMessage}
                  onKeywordClick={handleKeywordClick}
                  isGenerating={state.isGenerating}
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
