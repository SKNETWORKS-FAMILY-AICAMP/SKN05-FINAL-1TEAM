import styles from '@/app/styles/chat.module.css';
import { Keywords } from './Keywords';
import { SuggestedQuestions } from './SuggestedQuestions';

interface AIMessageProps {
  message: string;
  keywords: string[];
  suggestedQuestions: string[];
  onQuestionClick: (question: string) => void;
  onKeywordClick: (keyword: string) => void;
}

export function AIMessage({ 
  message, 
  keywords, 
  suggestedQuestions, 
  onQuestionClick,
  onKeywordClick
}: AIMessageProps) {
  return (
    <div className={styles.aiMessage}>
      <div className={styles.messageContent}>
        {message}
      </div>
      <hr className={styles.messageDivider} />
      <Keywords keywords={keywords} onKeywordClick={onKeywordClick} />
      <SuggestedQuestions 
        questions={suggestedQuestions}
        onQuestionClick={onQuestionClick}
      />
    </div>
  );
}
