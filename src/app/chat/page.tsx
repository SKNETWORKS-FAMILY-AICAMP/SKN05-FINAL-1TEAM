'use client';

import { useEffect, useState } from 'react';
import { SideBar } from '@/app/components/sidebar/SideBar';
import { Header } from '@/app/components/layout/Header';
import { ChatContainer } from '@/app/components/chat/ChatContainer';
import styles from '@/app/styles/chat.module.css';
import { useUserStore } from '@/app/store/userStore';
import { useSidebarStore } from '@/app/store/sidebarStore';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
  const { accessToken } = useUserStore();
  const router = useRouter();
  const { isOpen } = useSidebarStore();
  const [isMobile, setIsMobile] = useState<boolean>(false);

  useEffect(() => {
    // 화면 크기에 따라 모바일 여부 판단
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    handleResize(); // 초기 실행
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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
        <main
          className={styles.mainContent}
          style={{
            width: isMobile ? 'clac(100% - 3rem)' : isOpen ? 'calc(100% - 18rem - 3rem)' : 'clac(100% - 3rem)'
          }}
        >    
          <ChatContainer />
        </main>
      </div>
    </div>
  );
}
