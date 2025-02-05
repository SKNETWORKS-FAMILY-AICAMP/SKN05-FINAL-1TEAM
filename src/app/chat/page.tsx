'use client';

import { useEffect } from 'react';
import { SideBar } from '@/app/components/sidebar/SideBar';
import { Header } from '@/app/components/layout/Header';
import { ChatContainer } from '@/app/components/chat/ChatContainer';
import styles from '@/app/styles/chat.module.css';
import { useUserStore } from '../store/userStore';
import { useSidebarStore } from '../store/sidebarStore';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
  const { accessToken } = useUserStore();
  const router = useRouter();
  const { isOpen } = useSidebarStore();

  useEffect(() => {
    // 토큰이 없으면 로그인 페이지로 리다이렉트
    if (!accessToken) {
      router.push('/');
    }
  }, [accessToken, router]);

  if (!accessToken) {
    return null; // accessToken이 없으면 아무것도 렌더링하지 않음
  }

  return (
    <div className={styles.chatPage}>
      <Header />
      <div className={styles.contentContainer}>
        <SideBar />
        <main className={`${styles.mainContent} ${!isOpen ? styles.sidebarClosed : ''}`}>
          <ChatContainer />
        </main>
      </div>
    </div>
  );
}
