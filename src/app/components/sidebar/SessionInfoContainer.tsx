'use client';

import { useState, useEffect } from 'react';
import styles from '@/app/styles/sideBar.module.css';
import { useUserStore } from '@/app/store/userStore';

interface Session {
  sessionId: number;
  title: string;
  updatedAt: string;
}

export function SessionInfoContainer() {
  const { userId, username, email, accessToken } = useUserStore();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSessions = async () => {
      if (!userId || !accessToken) return;

      setIsLoading(true);
      try {
        // 세션 목록 가져오기
        const sessionResponse = await fetch(
          `http://localhost:8000/api/chat/sessionlist?userId=${userId}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${accessToken}`
            }
          }
        );

        if (!sessionResponse.ok) {
          throw new Error('Failed to fetch sessions');
        }

        const sessionData = await sessionResponse.json();
        setSessions(sessionData.session_list);
      } catch (error) {
        console.error('Error fetching sessions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSessions();
  }, [userId, accessToken]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      month: '2-digit',
      day: '2-digit',
    });
  };

  return (
    <div className={styles.container}>
      {isLoading ? (
        <div className={styles.loading}>로딩 중...</div>
      ) : (
        <>
          {/* 사용자 정보 섹션 */}
          <div className={styles.userInfo}>
            <h3 className={styles.username}>{username}</h3>
            <p className={styles.email}>{email}</p>
          </div>

          <hr className={styles.divider} />

          {/* 세션 목록 섹션 */}
          <div className={styles.sessionList}>
            {sessions.map((session) => (
              <button
                key={session.sessionId}
                className={styles.sessionButton}
                onClick={() => {
                  // 세션 선택 이벤트 발생
                  const event = new CustomEvent('sessionSelected', {
                    detail: session.sessionId
                  });
                  window.dispatchEvent(event);
                }}
              >
                <span className={styles.sessionTitle}>{session.title}</span>
                <span className={styles.sessionDate}>
                  {formatDate(session.updatedAt)}
                </span>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

