'use client';

import { useState, KeyboardEvent } from 'react';
import styles from '@/app/styles/chat.module.css';
import { useMessageStore } from '@/app/store/messageStore';
import { useUserStore } from '@/app/store/userStore';
import { useBrandStore } from '@/app/store/brandStore';
import HelpPopover from './HelpPopover';

export function ChatInput() {
  const [message, setMessage] = useState('');
  const [showHelp, setShowHelp] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { currentSession, setCurrentSession, addMessage } = useMessageStore();
  const { userId } = useUserStore();
  const { selectedBrand, selectedModel } = useBrandStore();

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading || !userId) return;

    const userMessage = message.trim();
    setMessage('');
    setIsLoading(true);

    try {
      // 사용자 메세지를 먼저 ChatContainer 에 추가
      
      const response = await fetch('http://localhost:8000/api/chat/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userMessage,
          userId: userId,
          sessionId: currentSession?.sessionId || null,
          brand: selectedBrand || null,
          model: selectedModel || null
        }),
      });

      const result = await response.json();

      if (!currentSession) {
        // 새 세션 생성
        const newSession = {
          sessionId: result.sessionId,
          userId: userId.toString(),
          title: userMessage.slice(0, 30) + "...",
          messages: [],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        };
        setCurrentSession(newSession);
      }

      // 새 메시지 추가
      const newMessage = {
        messageId: result.messageId,
        userMessage: userMessage,
        aiMessage: result.answer,
        keywords: result.keywords,
        suggestedQuestions: result.suggestQuestions
      };

      addMessage(newMessage);
    } catch (error) {
      console.error('Error sending message:', error);
      // 에러 발생 시 메시지 복원
      setMessage(userMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={styles.inputContainer}>
      <div className={styles.inputWrapper}>
        <button
          className={styles.helpButton}
          onClick={() => setShowHelp(!showHelp)}
          aria-label="도움말"
        >
          ?
        </button>
        <input
          className={styles.messageInput}
          placeholder={isLoading ? "응답을 기다리는 중..." : "메시지를 입력하세요"}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button
          className={`${styles.sendButton} ${isLoading ? styles.loading : ''}`}
          onClick={handleSendMessage}
          disabled={!message.trim() || isLoading}
        >
        </button>
      </div>
      {showHelp && <HelpPopover onClose={() => setShowHelp(false)} />}
    </div>
  );
}
