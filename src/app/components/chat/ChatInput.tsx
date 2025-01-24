'use client';

import { useState, KeyboardEvent } from 'react';
import styles from '@/app/styles/chat.module.css';
import { useMessageStore } from '@/app/store/messageStore';
import HelpPopover from './HelpPopover';

export function ChatInput() {
  const [message, setMessage] = useState('');
  const [showHelp, setShowHelp] = useState(false);
  const { currentSession, addMessage } = useMessageStore();

  const handleSendMessage = async () => {
    if (!message.trim() || !currentSession) return;

    try {
      const response = await fetch('http://localhost:8000/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        body: JSON.stringify({
          sessionId: currentSession.sessionId,
          userMessage: message.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const newMessage = await response.json();
      addMessage(newMessage);
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
      // 여기에 에러 처리 로직 추가 가능
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
          placeholder="메시지를 입력하세요"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button
          className={styles.sendButton}
          onClick={handleSendMessage}
          disabled={!message.trim() || !currentSession}
        >
          전송
        </button>
      </div>
      {showHelp && <HelpPopover onClose={() => setShowHelp(false)} />}
    </div>
  );
}
