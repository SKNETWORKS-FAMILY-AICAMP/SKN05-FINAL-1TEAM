'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from '../styles/register.module.css';
import { BASE_URL } from '@/config';

const API_URL = `${BASE_URL}/api/user/create`;

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [formError, setFormError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');
    setSuccessMessage('');

    // 유효성 검사
    if (!formData.name || !formData.email || !formData.password) {
      setFormError('모든 필수 항목을 입력해주세요.');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setFormError('비밀번호가 일치하지 않습니다.');
      return;
    }

    try {
      // FastAPI 엔드포인트에 POST 요청 보내기
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.name,
          email: formData.email,
          password1: formData.password,
          password2: formData.confirmPassword
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || '회원가입 실패');
      }

      setSuccessMessage('회원가입에 성공했습니다! 이제 로그인하세요.');
      // 회원가입 성공 시 로그인 페이지로 이동
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } catch (error: any) {
      setFormError(error.message || '회원가입 중 문제가 발생했습니다.');
    }
  };

  return (
    <div className={styles.registerContainer}>
      <div className={styles.registerFormWrapper}>
        <h2 className={styles.registerTitle}>회원가입</h2>
        <form className={styles.registerForm} onSubmit={handleSubmit}>
          {formError && <p className={styles.registerError}>{formError}</p>}
          {successMessage && <p className={styles.registerSuccess}>{successMessage}</p>}

          <div className={styles.formFieldsContainer}>
            <div>
              <label htmlFor="name" className={styles.formLabel}>
                이름
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                className={styles.formInput}
                placeholder="이름을 입력하세요"
                value={formData.name}
                onChange={handleChange}
              />
            </div>

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
                placeholder="이메일을 입력하세요"
                value={formData.email}
                onChange={handleChange}
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
                placeholder="비밀번호를 입력하세요"
                value={formData.password}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className={styles.formLabel}>
                비밀번호 확인
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                className={styles.formInput}
                placeholder="비밀번호를 입력하세요"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
            </div>
          </div>

          <button type="submit" className={styles.submitButton}>
            회원가입
          </button>
        </form>
        <div className={styles.loginRedirect}>
          이미 계정이 있으신가요?{' '}
          <button
            onClick={() => router.push('/login')}
            className={styles.inlineButton}
          >
            로그인 하러가기
          </button>
        </div>
      </div>
    </div>
  );
}
