import styles from '@/app/styles/chat.module.css';

interface SuggestedQuestionsProps {
  questions: string[];
  onQuestionClick: (question: string) => void;
}

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