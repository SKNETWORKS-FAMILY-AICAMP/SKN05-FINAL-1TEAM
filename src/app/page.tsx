'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // 홈 페이지에 들어오면 자동으로 채팅 페이지로 리다이렉트
    router.push('/chat');
  }, [router]);

  return null; // 렌더링할 내용이 없으므로 null 반환
}
