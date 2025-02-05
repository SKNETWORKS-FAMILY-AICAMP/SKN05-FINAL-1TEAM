'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUserStore } from '@/app/store/userStore';

export default function Home() {
  const router = useRouter();
  const { accessToken, setAccessToken, setUser } = useUserStore();

  useEffect(() => {
    // 로컬 스토리지에서 access token과 사용자 정보 불러오기
    const token = localStorage.getItem('accessToken');
    const userId = localStorage.getItem('userId');
    const username = localStorage.getItem('username');
    const email = localStorage.getItem('email');

    if (token) {
      setAccessToken(token); // 상태 업데이트
    }

    if (userId && username && email) {
      setUser(userId, username, email); // token 매개변수 제거
    }

    // accessToken이 설정된 후에 리다이렉트 처리
    if (token) {
      router.push('/chat'); // accessToken이 있을 경우 채팅 페이지로 이동
    } else {
      router.push('/login'); // accessToken이 없으면 로그인 페이지로 이동
    }
  }, [router, setAccessToken, setUser]);

  return null; // 렌더링할 내용이 없으므로 null 반환
}
