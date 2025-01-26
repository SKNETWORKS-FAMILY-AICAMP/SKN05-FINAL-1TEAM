'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from '../styles/login.module.css';
import { useUserStore } from '../store/userStore';

const API_URL = 'http://localhost:8000/api/user/login';

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({ email: '', password: ''});
  const [formError, setFormError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setFormError('');
    setSuccessMessage('');

    if (!formData.email || !formData.password) {
      setFormError('이메일과 비밀번호를 입력하세요.');
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || '로그인에 실패했습니다.');
      }

      // userStore 업데이트
      useUserStore.getState().setUser(
        data.userId,
        data.username,
        data.email,
        data.access_token
      );

      setSuccessMessage('로그인 성공! 메인 페이지로 이동합니다.');
      setTimeout(() => {
        router.push('/chat');
      }, 2000);
    } catch (error: any) {
      setFormError(error.message || '로그인 중 문제가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.loginContainer}>
      <div className={styles.loginFormWrapper}>
        <h2 className={styles.loginTitle}>로그인</h2>
        <form className={styles.loginForm} onSubmit={handleSubmit}>
          {formError && <p className={styles.loginError}>{formError}</p>}
          {successMessage && <p className={styles.loginSuccess}>{successMessage}</p>}

          <div className={styles.formFieldsContainer}>
            <div>
              <label htmlFor="email" className={styles.formLabel}>
                아이디(이메일)
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className={styles.formInput}
                value={formData.email}
                onChange={handleChange}
                placeholder="이메일을 입력하세요"
              />
            </div>

            <div>
              <label htmlFor="password" className={styles.formLabel}>
                비밀번호
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className={styles.formInput}
                value={formData.password}
                onChange={handleChange}
                placeholder="비밀번호를 입력하세요"
              />
            </div>
          </div>

          <button type="submit" className={styles.submitButton} disabled={isLoading}>
            로그인
          </button>
        </form>
        <div className={styles.registerRedirect}>
          계정이 없으신가요?{' '}
          <button
            onClick={() => router.push('/register')}
            className={styles.registerButton}
          >
            회원가입 하러가기
          </button>
        </div>
      </div>
    </div>
  );
}
