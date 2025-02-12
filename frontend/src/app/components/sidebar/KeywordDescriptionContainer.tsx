'use client';

import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import styles from '@/app/styles/sideBar.module.css';

interface KeywordDescription {
  keyword: string;
  description: string;
}

export function KeywordDescriptionContainer() {
  const [currentKeyword, setCurrentKeyword] = useState<KeywordDescription | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchKeywordDescription = async (keyword: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/chat/keyword?keyword=${encodeURIComponent(keyword)}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || '키워드 설명을 가져오는데 실패했습니다.');
      }

      setCurrentKeyword({
        keyword: keyword,
        description: data.description
      });
    } catch (error) {
      console.error('Error fetching keyword description:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // CustomEvent 리스너 추가
  useEffect(() => {
    const handleKeywordSelected = (event: CustomEvent<string>) => {
      fetchKeywordDescription(event.detail);
    };

    window.addEventListener('keywordSelected', handleKeywordSelected as EventListener);

    return () => {
      window.removeEventListener('keywordSelected', handleKeywordSelected as EventListener);
    };
  }, []);

  return (
    <div className={styles.container}>
      {/* <h2 className={styles.containerTitle}>키워드 설명</h2> */}
      {isLoading ? (
        <div className={styles.loading}>로딩 중...</div>
      ) : currentKeyword ? (
        <>
          <h4 className={styles.keywordName}>#{currentKeyword.keyword}</h4>
          <hr className={styles.divider} />
          <div className={styles.keywordDescription}>
            <ReactMarkdown>{currentKeyword.description}</ReactMarkdown>
          </div>
        </>
      ) : (
        <p className={styles.emptyMessage}>키워드를 클릭하면 설명이 표시됩니다.</p>
      )}
    </div>
  );
}