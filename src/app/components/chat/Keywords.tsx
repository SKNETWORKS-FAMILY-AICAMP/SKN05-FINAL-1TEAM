import styles from '@/app/styles/chat.module.css';

interface KeywordsProps {
  keywords: string[];
}

export function Keywords({ keywords }: KeywordsProps) {
  return (
    <div className={styles.keywordsContainer}>
      {keywords.map((keyword, index) => (
        <button key={index} className={styles.keywordTag}>
          #{keyword}
        </button>
      ))}
    </div>
  );
} 