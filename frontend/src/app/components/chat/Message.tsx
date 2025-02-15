import styles from '@/app/styles/chat.module.css';
import { Keywords, SuggestedQuestions } from './PlusMessage';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface UserMessageProps {
  message: string;
}

interface AIMessageProps {
    message: string;
    keywords: string[];
    suggestedQuestions: string[];
    onQuestionClick: (question: string) => void;
    onKeywordClick: (keyword: string) => void;
    isGenerating?: boolean;
}

// usermessage
export function UserMessage({ message }: UserMessageProps) {
  return (
    <div className={styles.userMessage}>
      <div className={styles.messageContent}>
        {message}
      </div>
    </div>
  );
}

//ai message
export function AIMessage({ 
  message, 
  keywords, 
  suggestedQuestions, 
  onQuestionClick,
  onKeywordClick,
  isGenerating = false
}: AIMessageProps) {
  return (
    <div className={styles.aiMessage}>
      <div className={styles.markdown_body}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {message}
        </ReactMarkdown>
        {/* {message} */}
        {isGenerating && <span className={styles.cursor}>|</span>}
      </div>
      {!isGenerating && keywords.length > 0 && (
        <>
          <hr className={styles.messageDivider} />
          <Keywords keywords={keywords} onKeywordClick={onKeywordClick} />
          <SuggestedQuestions 
            questions={suggestedQuestions}
            onQuestionClick={onQuestionClick}
          />
        </>
      )}
    </div>
  );
}