'use client';

import { useEffect } from 'react';
import { useSidebarStore } from '@/app/store/sidebarStore';
import styles from '@/app/styles/sideBar.module.css';
import { SessionInfoContainer } from '@/app/components/sidebar/SessionInfoContainer';
import { ModelSelectContainer } from '@/app/components/sidebar/ModelSelectContainer';
import { KeywordDescriptionContainer } from '@/app/components/sidebar/KeywordDescriptionContainer';
import { FaBars, FaChevronLeft, FaComments, FaCamera, FaKeyboard } from 'react-icons/fa';

export function SideBar() {
  const { isOpen, toggle, setIsOpen } = useSidebarStore();

  // 화면 크기에 따른 사이드바 상태 관리
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setIsOpen(false); // 화면이 작아지면 자동으로 미니 사이드바로
      } else {
        setIsOpen(true); // 화면이 커지면 자동으로 펼쳐진 사이드바로
      }
    };

    // 초기 실행
    handleResize();

    // 리사이즈 이벤트 리스너
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [setIsOpen]);

  // 토글 버튼 컴포넌트
  const ToggleButton = () => (
    <button 
      className={styles.toggleButton} 
      onClick={toggle}
      aria-label="Toggle Sidebar"
    >
      {isOpen ? <FaChevronLeft size={20} /> : <FaBars size={20} />}
    </button>
  );

  return (
    <div className={`${styles.sideBar} ${isOpen ? styles.open : styles.closed}`}>
      <div className={styles.toggleButtonContainer}>
        <ToggleButton />
      </div>
        {isOpen ? (
        // 펼쳐진 사이드바
        <>
          <SessionInfoContainer />
          <ModelSelectContainer />
          <KeywordDescriptionContainer />
        </>
      ) : (
        // 미니 사이드바
        <div className={styles.miniSidebar}>
          <button className={styles.miniButton} title="Sessions">
            <FaComments size={20} />
          </button>
          <button className={styles.miniButton} title="Camera Model">
            <FaCamera size={20} />
          </button>
          <button className={styles.miniButton} title="Keywords">
            <FaKeyboard size={20} />
          </button>
        </div>
      )}
    </div>
  );
}
