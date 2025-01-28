'use client';

import { useState, useEffect, useCallback } from 'react';
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
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);

  // 세션 목록을 불러오는 함수
  const fetchSessions = useCallback(async () => {
    if (!userId || !accessToken) return;

    setIsLoading(true);
    try {
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
      console.log('Fetched sessions:', sessionData.session_list); // 디버깅용
      setSessions(sessionData.session_list);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    } finally {
      setIsLoading(false);
    }
  }, [userId, accessToken]);

  // 새 대화 시작 핸들러
  const handleNewChat = () => {
    setCurrentSessionId(null);
    const event = new CustomEvent('startNewChat');
    window.dispatchEvent(event);
  };

  // 세션 선택 이벤트 리스너
  useEffect(() => {
    const handleSessionSelected = (event: CustomEvent<number>) => {
      setCurrentSessionId(event.detail);
    };

    window.addEventListener('sessionSelected', handleSessionSelected as EventListener);

    return () => {
      window.removeEventListener('sessionSelected', handleSessionSelected as EventListener);
    };
  }, []);

  // 초기 로딩
  useEffect(() => {
    fetchSessions();
  }, [userId, accessToken]);

  // 새 세션 생성 이벤트 리스너
  useEffect(() => {
    const handleSessionCreated = (event: Event) => {
      const customEvent = event as CustomEvent<{ sessionId: number }>;
      console.log('Session created event received:', customEvent.detail); // 디버깅용
      fetchSessions();
    };

    window.addEventListener('sessionCreated', handleSessionCreated);

    return () => {
      window.removeEventListener('sessionCreated', handleSessionCreated);
    };
  }, [fetchSessions]);

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
          <div className={styles.headerRow}>
            <div className={styles.userInfo}>
              <h3 className={styles.username}>{username}</h3>
              <p className={styles.email}>{email}</p>
            </div>
            <button 
              className={styles.newChatButton}
              onClick={handleNewChat}
              title="새 대화 시작"
            >
              + New
            </button>
          </div>

          <hr className={styles.divider} />

          {/* 세션 목록 섹션 */}
          <div className={styles.sessionList}>
            {sessions.map((session) => (
              <button
                key={session.sessionId}
                className={`${styles.sessionButton} ${
                  currentSessionId === session.sessionId ? styles.activeSession : ''
                }`}
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

