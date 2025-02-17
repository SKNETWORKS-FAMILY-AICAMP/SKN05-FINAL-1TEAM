'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import styles from '@/app/styles/chat.module.css';
import { ChatInput } from './ChatInput';
// import { UserMessage } from './UserMessage';
// import { AIMessage } from './AIMessage';
import { UserMessage, AIMessage } from './Message';
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

export function ChatContainer() {
  // ref
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const keywordsRef = useRef([]);
  const suggestQuestionsRef = useRef([]);

  // Store hooks
  const { accessToken } = useUserStore();
  const { selectedBrand, selectedModel } = useBrandStore();

  // state
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [currentAnswer, setCurrentAnswer] = useState<string>("");
  const [currentNodes, setCurrentNodes] = useState<{ message_id: number; currentNodes: string[]; }>({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [isReverseQ, setIsReverseQ] = useState(false);


  // 자동 스크롤
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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

      if (!response.ok) throw new Error('Failed to load session history');

      const data = await response.json();
      if (data.Messages && Array.isArray(data.Messages)) {
        console.log('Received messages:', data.Messages); // 디버깅용
        setMessages(data.Messages.map((msg: any) => ({
            message_id: msg.message_id,
            userMessage: msg.userMessage,
            aiMessage: msg.aiMessage,
            keywords: msg.keywords || [],
            suggestQuestions: msg.suggestQuestions || []
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

    // 세션 선택, 새 채팅 이펙트
    useEffect(() => {
      const handleSessionSelected = (event: CustomEvent<number>) => {
        loadSessionHistory(event.detail);
      };
  
      const handleNewChat = () => {
        setCurrentSessionId(null);
        setMessages([]);
      };
  
      window.addEventListener('sessionSelected', handleSessionSelected as EventListener);
      window.addEventListener('startNewChat', handleNewChat);
  
      return () => {
        window.removeEventListener('sessionSelected', handleSessionSelected as EventListener);
        window.removeEventListener('startNewChat', handleNewChat);
      };
    }, [loadSessionHistory]);

  // 스트림 응답 처리
  const handleStreamResponse = async (reader: ReadableStreamDefaultReader<Uint8Array>, decoder: TextDecoder, userMessageId: number) => {
    let accumulatedAnswer = "";
    let accumulatedNode = { message_id: 0, currentNodes: [] };
    let buffer = "";

    const updateNodeState = (data: any) => {
      if (accumulatedNode.currentNodes.at(-1) !== data.currentNode) {
        accumulatedNode.currentNodes.push(data.currentNode);
        setCurrentNodes({
          message_id: userMessageId,
          currentNodes: [...accumulatedNode.currentNodes]
        });
      }
    };

    const handleGenerationInProgress = (data: any) => {
      accumulatedAnswer += data.answer;
      setCurrentAnswer(accumulatedAnswer);
      updateNodeState(data);
    };

    const handleRefinementOrCamera = (data: any) => {
      accumulatedAnswer += data.answer;
      setCurrentAnswer(accumulatedAnswer);
      
      accumulatedNode.currentNodes.push("END");
      setCurrentNodes({
        message_id: userMessageId,
        currentNodes: [...accumulatedNode.currentNodes]
      });
      
      setMessages(prev => prev.map(msg =>
        msg.message_id === userMessageId
          ? {
              ...msg,
              aiMessage: accumulatedAnswer,
              keywords: [...(keywordsRef.current || [])],
              suggestQuestions: [...(keywordsRef.current || [])]
            }
          : msg
      ));
      setCurrentAnswer("");
      setIsGenerating(false);
      setIsReverseQ(data.currentNode === "질문 준비 중");
    };

    const handleFinalMessage = (data: any) => {
      console.log('Final message data:', data); // 최종 데이터 확인
      updateNodeState(data);

      if (Array.isArray(data.keywords) && data.keywords.length > 0) {
        keywordsRef.current = data.keywords;
      }
      if (Array.isArray(data.suggestQuestions) && data.suggestQuestions.length > 0) {
        suggestQuestionsRef.current = data.suggestQuestions;
      }

      // 두 데이터가 모두 수집되었는지 확인
      if (keywordsRef.current.length > 0 && suggestQuestionsRef.current.length > 0) {
        const finalKeywords = [...keywordsRef.current];
        const finalSuggestQuestions = [...suggestQuestionsRef.current];
        
        setCurrentNodes({
          message_id: userMessageId,
          currentNodes: ["END"]
        });   
        
        setMessages(prev => prev.map(msg =>
          msg.message_id === userMessageId
            ? {
                ...msg,
                aiMessage: accumulatedAnswer,
                keywords: finalKeywords,
                suggestQuestions: finalSuggestQuestions
              }
            : msg
        ));
        
        setCurrentAnswer("");
        setIsGenerating(false);
      }
    };  

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

          // 세션 ID 처리 로직 개선
          if (data.sessionId) {
            setCurrentSessionId(data.sessionId);
            
            // 새 세션이 생성된 경우 이벤트 발생
            if (!currentSessionId) {
              const event = new CustomEvent('sessionCreated', {
                detail: { sessionId: data.sessionId }
              });
              window.dispatchEvent(event);
            }
          }
          if (data.currentNode === "답변 생성 중") {
            handleGenerationInProgress(data);
          } else if (data.currentNode === "질문 재검색") {
            // 답변 초기화
            accumulatedAnswer = "";
            setCurrentAnswer("");
            updateNodeState(data);
          } else if (data.currentNode === "질문 준비 중" || data.currentNode === "not_for_camera") {
            handleRefinementOrCamera(data);
          } else {
            handleFinalMessage(data);
          }

        } catch (error) {
          console.error('Error parsing line:', line, error);
        }
      }
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!accessToken || isLoading) return;

    setIsLoading(true);
    setIsGenerating(true);
    setCurrentAnswer("");
    setIsReverseQ(false);
    keywordsRef.current = [];
    suggestQuestionsRef.current = [];
    
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
      session_id: currentSessionId,  // null일 때만 undefined로 처리됨
      brand: selectedBrand || "",
      model: selectedModel || ""
    };

    // null인 경우에만 session_id 제거
    if (currentSessionId === null) {
      delete requestData.session_id;
    }

    console.log('Request data:', requestData);
    
    try {
      const endpoint = isReverseQ ? 'rqanswer' : 'answer';
      const response = await fetch(`http://localhost:8000/api/chat/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(requestData),
      });

      if (isReverseQ) setIsReverseQ(false);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Request failed: ${JSON.stringify(errorData)}`);
      }

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      await handleStreamResponse(reader, decoder, userMessageId)
    } catch (error) {
      console.error('Error sending message:', error);
      setCurrentAnswer("오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeywordClick = (keyword: string) => {
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
                    <ProgressStep currentNodes={currentNodes.currentNodes} />
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