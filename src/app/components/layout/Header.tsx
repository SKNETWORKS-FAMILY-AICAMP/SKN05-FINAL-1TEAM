'use client';

import styles from '@/app/styles/header.module.css';
import { useUserStore } from '@/app/store/userStore'; // userStore를 가져오는 경로를 수정하세요.
import { useRouter } from 'next/navigation'; // useRouter를 가져옵니다.

export function Header() {
  const { accessToken } = useUserStore(); // userStore에서 accessToken을 가져옵니다.
  const router = useRouter(); // useRouter 훅을 사용합니다.

  const handleLogin = () => {
    router.push('/login'); // 로그인 버튼 클릭 시 /login으로 이동합니다.
  };

  const handleLogout = () => {
    router.push('/login'); // 로그아웃 후 /login으로 이동
  };

  return (
    <header className={styles.header}>
      <h1 className={styles.headerTitle}>CARAGSER</h1>
      {accessToken ? (
        <button className={styles.logoutButton} onClick={handleLogout}>Logout</button>
      ) : (
        <button className={styles.loginButton} onClick={handleLogin}>Login</button> // 로그인 버튼 클릭 시 handleLogin 호출
      )}
    </header>
  );
}