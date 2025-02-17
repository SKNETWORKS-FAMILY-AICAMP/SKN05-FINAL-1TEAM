import styles from '@/app/styles/chat.module.css';

interface KeywordsProps {
  keywords: string[];
  onKeywordClick: (keyword: string) => void;
}

interface SuggestedQuestionsProps {
    questions: string[];
    onQuestionClick: (question: string) => void;
  }

// 키워드 컴포넌트
export function Keywords({ keywords, onKeywordClick }: KeywordsProps) {
  return (
    <div className={styles.keywordsContainer}>
      {keywords.map((keyword, index) => (
        <button
          key={`${keyword}-${index}`}
          className={styles.keywordTag}
          onClick={() => onKeywordClick(keyword)}
        >
          #{keyword}
        </button>
      ))}
    </div>
  );
} 

// question 컴포넌트
export function SuggestedQuestions({ questions, onQuestionClick }: SuggestedQuestionsProps) {
  return (
    <div className={styles.suggestedQuestionsContainer}>
        <div className={styles.suggestedQuestions}>
            {questions.map((question, index) => (
                <button
                    key={index}
          className={styles.suggestedQuestion}
          onClick={() => onQuestionClick(question)}
        >
                    {question}
                </button>
            ))}
        </div>
    </div>
  );
} 