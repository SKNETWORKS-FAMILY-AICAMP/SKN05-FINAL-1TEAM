'use client';

import { useEffect } from 'react';
import { SideBar } from '@/app/components/sidebar/SideBar';
import { Header } from '@/app/components/layout/Header';
import { ChatContainer } from '@/app/components/chat/ChatContainer';
import styles from '@/app/styles/chat.module.css';
import { useMessageStore } from '../store/messageStore';
import { useUserStore } from '../store/userStore';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
  const { setCurrentSession } = useMessageStore();

  useEffect(() => {
    // 테스트용 임시 세션 생성
    const mockSession = {
      sessionId: "test-session-1",
      userId: "test-user",
      title: "테스트 세션",
      messages: [
        {
          messageId: "msg1",
          userMessage: "카메라 설정하는 방법 알려줘",
          aiMessage: "카메라 설정은 다음과 같은 단계로 진행할 수 있습니다:\n1. 메뉴 버튼을 눌러주세요\n2. 설정 메뉴로 이동합니다\n3. 원하는 설정을 조정하세요",
          keywords: ["카메라", "설정", "메뉴"],
          suggestedQuestions: [
            "셔터 스피드는 어떻게 조절하나요?",
            "ISO 감도 설정은 어디서 하나요?",
            "화이트밸런스 조정 방법이 궁금해요"
          ],
          createdAt: new Date().toISOString()
        },
        {
          messageId: "msg2",
          userMessage: "셔터 스피드는 어떻게 조절하나요?",
          aiMessage: "셔터 스피드 조절 방법입니다:\n1. 모드 다이얼을 S나 M으로 설정합니다\n2. 메인 다이얼을 돌려 원하는 셔터 스피드를 선택합니다\n3. 빠른 셔터 스피드는 움직임을 멈추게 하고, 느린 셔터 스피드는 움직임을 표현합니다",
          keywords: ["셔터스피드", "모드다이얼", "카메라설정"],
          suggestedQuestions: [
            "조리개 값은 어떻게 조절하나요?",
            "manual 모드는 어떻게 사용하나요?",
            "셔터 우선 모드의 장점이 뭔가요?"
          ],
          createdAt: new Date().toISOString()
        }
      ],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    setCurrentSession(mockSession);
  }, [setCurrentSession]);

  // const { accessToken } = useUserStore();
  // const router = useRouter();

  // useEffect(() => {
  //   const createNewSession = async () => {
  //     try {
  //       if (!accessToken) {
  //         router.push('/login');
  //         return;
  //       }

  //       const response = await fetch('http://localhost:8000/api/sessions', {
  //         method: 'POST',
  //         headers: {
  //           'Content-Type': 'application/json',
  //           'Authorization': `Bearer ${accessToken}`,
  //         },
  //         body: JSON.stringify({
  //           title: "새로운 대화",
  //         }),
  //       });

  //       if (!response.ok) {
  //         throw new Error('Failed to create session');
  //       }

  //       const session = await response.json();
  //       setCurrentSession(session);
  //     } catch (error) {
  //       console.error('Error creating session:', error);
  //     }
  //   };

  //   createNewSession();
  // }, [setCurrentSession, router]);

  return (
    <div className={styles.chatPage}>
      <Header />
      <div className={styles.contentContainer}>
        <SideBar />
        <ChatContainer />
      </div>
    </div>
  );
}
