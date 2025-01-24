import styles from '@/app/styles/chat.module.css';

interface KeywordsProps {
  keywords: string[];
  onKeywordClick: (keyword: string) => void;
}

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