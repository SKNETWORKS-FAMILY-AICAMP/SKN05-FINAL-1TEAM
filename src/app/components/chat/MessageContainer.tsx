import { useMessageStore } from '@/app/store/messageStore';
import { useUserStore } from '@/app/store/userStore';
import styles from '@/app/styles/chat.module.css';
import { Keywords } from './Keywords';
import { SuggestedQuestions } from './SuggestedQuestions';
import { useState } from 'react';

interface PendingMessage {
  messageId: string;
  userMessage: string;
}

export function MessageContainer() {
  const { currentSession, addMessage } = useMessageStore();
  const { userId } = useUserStore();
  const [pendingMessage, setPendingMessage] = useState<PendingMessage | null>(null);

  const handleQuestionClick = async (question: string) => {
    if (!currentSession || !userId) return;
    
    try {
      // 먼저 pending 상태 설정
      setPendingMessage({
        messageId: `pending-${Date.now()}`,
        userMessage: question
      });

      const response = await fetch('http://localhost:8000/api/chat/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          userId: userId,
          sessionId: currentSession.sessionId,
          brand: null,
          model: null
        }),
      });

      const result = await response.json();

      // 새 메시지 추가
      const newMessage = {
        messageId: result.messageId,
        userMessage: question,
        aiMessage: result.answer,
        keywords: result.keywords,
        suggestedQuestions: result.suggestQuestions
      };

      addMessage(newMessage);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setPendingMessage(null);
    }
  };

  const messages = currentSession?.messages || [];
  const allMessages = pendingMessage 
    ? [...messages, pendingMessage]
    : messages;

  return (
    <div className={styles.messagesWrapper}>
      {allMessages.map((message, index) => (
        <div 
          key={`message-${message.messageId}-${index}`} 
          className={styles.messageGroup}
        >
          <div className={styles.userMessage}>
            <div className={styles.messageContent}>
              {message.userMessage}
            </div>
          </div>

          {'aiMessage' in message ? (
            <div className={styles.aiMessage}>
              <div className={styles.messageContent}>
                {message.aiMessage}
              </div>
              <hr className={styles.messageDivider} />
              <Keywords keywords={message.keywords} />
              <SuggestedQuestions 
                questions={message.suggestedQuestions}
                onQuestionClick={handleQuestionClick}
              />
            </div>
          ) : (
            <div className={`${styles.aiMessage} ${styles.loading}`}>
              <div className={styles.messageContent}>
                <div className={styles.loadingDots}>응답 생성 중...</div>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
} 