import { useState, KeyboardEvent } from 'react';
import styles from '@/app/styles/chat.module.css';
import HelpPopover from './HelpPopover';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [showHelp, setShowHelp] = useState(false);

  const handleSendMessage = () => {
    if (!message.trim() || isLoading) return;
    onSend(message.trim());
    setMessage('');
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
        <button onClick={() => setShowHelp(!showHelp)} className={styles.helpButton}>
          ?
        </button>
        <input
          className={styles.messageInput}
          placeholder={isLoading ? '응답을 기다리는 중...' : '메시지를 입력하세요'}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button
          onClick={handleSendMessage}
          disabled={!message.trim() || isLoading}
          className={`${styles.sendButton} ${isLoading ? styles.loading : ''}`}
        >
          전송
        </button>
      </div>
      {showHelp && <HelpPopover onClose={() => setShowHelp(false)} />}
    </div>
  );
}
