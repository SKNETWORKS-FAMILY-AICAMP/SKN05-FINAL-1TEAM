'use client';

import { useState } from 'react';
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
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { userId } = useUserStore();
  const { selectedBrand, selectedModel } = useBrandStore();
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);


  const handleSendMessage = async (message: string) => {
    if (!userId || isLoading) return;

    setIsLoading(true);
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

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.detail || 'Failed to send message');
      }

      // 첫 메시지인 경우 세션 ID 저장
      if (!currentSessionId) {
        setCurrentSessionId(result.sessionId);
      }

      const newMessage: Message = {
        messageId: result.messageId,
        userMessage: message,
        aiMessage: result.answer,
        keywords: result.keywords,
        suggestedQuestions: result.suggestQuestions
      };

      setMessages(prev => [...prev, newMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // 사용자에게 에러 메시지를 보여줄 수 있습니다
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
              <AIMessage 
                message={message.aiMessage}
                keywords={message.keywords}
                suggestedQuestions={message.suggestedQuestions}
                onQuestionClick={handleSendMessage}
                onKeywordClick={handleKeywordClick}
              />
            </div>
          ))}
        </div>
      </div>
      <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
