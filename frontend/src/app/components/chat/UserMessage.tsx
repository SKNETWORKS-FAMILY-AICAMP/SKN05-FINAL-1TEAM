import styles from '@/app/styles/chat.module.css';

interface UserMessageProps {
  message: string;
}

export function UserMessage({ message }: UserMessageProps) {
  return (
    <div className={styles.userMessage}>
      <div className={styles.messageContent}>
        {message}
      </div>
    </div>
  );
}
