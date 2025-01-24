import styles from '@/app/styles/chat.module.css';
import { ChatInput } from './ChatInput';
import { MessageContainer } from './MessageContainer';

export function ChatContainer() {
  return (
    <div className={styles.chatContainer}>
      <div className={styles.messagesContainer}>
        <MessageContainer />
      </div>
      <ChatInput />
    </div>
  );
}
