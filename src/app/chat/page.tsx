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

  // useEffect(() => {
  //   // 테스트용 임시 세션 생성
  //   const mockSession = {
  //     sessionId: "test-session-1",
  //     userId: "test-user",
  //     title: "테스트 세션",
  //     messages: [
  //       {
  //         messageId: "msg1",
  //         userMessage: "카메라 설정하는 방법 알려줘",
  //         aiMessage: "카메라 설정은 다음과 같은 단계로 진행할 수 있습니다:\n1. 메뉴 버튼을 눌러주세요\n2. 설정 메뉴로 이동합니다\n3. 원하는 설정을 조정하세요",
  //         keywords: ["카메라", "설정", "메뉴"],
  //         suggestedQuestions: [
  //           "셔터 스피드는 어떻게 조절하나요?",
  //           "ISO 감도 설정은 어디서 하나요?",
  //           "화이트밸런스 조정 방법이 궁금해요"
  //         ],
  //         createdAt: new Date().toISOString()
  //       },
  //       {
  //         messageId: "msg2",
  //         userMessage: "셔터 스피드는 어떻게 조절하나요?",
  //         aiMessage: "셔터 스피드 조절 방법입니다:\n1. 모드 다이얼을 S나 M으로 설정합니다\n2. 메인 다이얼을 돌려 원하는 셔터 스피드를 선택합니다\n3. 빠른 셔터 스피드는 움직임을 멈추게 하고, 느린 셔터 스피드는 움직임을 표현합니다",
  //         keywords: ["셔터스피드", "모드다이얼", "카메라설정"],
  //         suggestedQuestions: [
  //           "조리개 값은 어떻게 조절하나요?",
  //           "manual 모드는 어떻게 사용하나요?",
  //           "셔터 우선 모드의 장점이 뭔가요?"
  //         ],
  //         createdAt: new Date().toISOString()
  //       }
  //     ],
  //     createdAt: new Date().toISOString(),
  //     updatedAt: new Date().toISOString()
  //   };

  //   setCurrentSession(mockSession);
  // }, [setCurrentSession]);

  const { accessToken, userId } = useUserStore();
  const router = useRouter();

  useEffect(() => {
    // 토큰이 없으면 로그인 페이지로 리다이렉트
    if (!accessToken) {
      router.push('/login');
      return;
    }

    // 세션 목록 가져오기
    const fetchSessions = async () => {
      try {
        // API 서버가 실행 중인지 확인
        const response = await fetch('http://localhost:8000/api/chat/sessionlist?userId=' + userId, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 필요한 경우 Authorization 헤더 추가
            'Authorization': `Bearer ${accessToken}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.session_list && data.session_list.length > 0) {
          // 가장 최근 세션을 현재 세션으로 설정
          const latestSession = data.session_list[0];
          
          // 채팅 기록 가져오기
          const historyResponse = await fetch(
            `http://localhost:8000/api/chat/history?userId=${userId}&sessionId=${latestSession.sessionId}`,
            {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
              }
            }
          );

          if (!historyResponse.ok) {
            throw new Error(`HTTP error! status: ${historyResponse.status}`);
          }

          const historyData = await historyResponse.json();
          
          // 세션 데이터 구성
          const sessionData = {
            sessionId: latestSession.sessionId,
            userId: userId?.toString(),
            title: latestSession.title,
            messages: historyData.Messages,
            createdAt: latestSession.createdAt,
            updatedAt: latestSession.updatedAt
          };
          
          setCurrentSession(sessionData);
        }
      } catch (error) {
        console.error('Error fetching sessions:', error);
        // 에러 처리 - 사용자에게 알림을 보여줄 수 있습니다
      }
    };

    if (userId) {
      fetchSessions();
    }
  }, [accessToken, userId, router, setCurrentSession]);

  // accessToken이 없으면 로그인 페이지로 리다이렉트
  if (!accessToken) {
    return null;
  }

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
