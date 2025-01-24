import { useMessageStore } from '@/app/store/messageStore';
import styles from '@/app/styles/chat.module.css';
import { Keywords } from './Keywords';
import { SuggestedQuestions } from './SuggestedQuestions';

export function MessageContainer() {
  const { currentSession, addMessage } = useMessageStore();

  const handleQuestionClick = async (question: string) => {
    if (!currentSession) return;
    
    try {
      const response = await fetch('http://localhost:8000/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        body: JSON.stringify({
          sessionId: currentSession.sessionId,
          userMessage: question,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const newMessage = await response.json();
      addMessage(newMessage);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className={styles.messagesWrapper}>
      {currentSession?.messages.map((message) => (
        <div key={message.messageId} className={styles.messageGroup}>
          <div className={styles.userMessage}>
            <div className={styles.messageContent}>
              {message.userMessage}
            </div>
          </div>

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
        </div>
      ))}
    </div>
  );
} 