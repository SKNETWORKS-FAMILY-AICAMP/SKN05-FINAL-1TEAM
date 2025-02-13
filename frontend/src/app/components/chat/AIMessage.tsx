import styles from '@/app/styles/chat.module.css';
import { Keywords } from './Keywords';
import { SuggestedQuestions } from './SuggestedQuestions';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';

interface AIMessageProps {
  message: string;
  keywords: string[];
  suggestedQuestions: string[];
  onQuestionClick: (question: string) => void;
  onKeywordClick: (keyword: string) => void;
  isGenerating?: boolean;
}

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
        <ReactMarkdown>
          {message}
        </ReactMarkdown>
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