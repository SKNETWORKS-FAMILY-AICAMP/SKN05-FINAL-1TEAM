'use client';

import { useEffect, useRef, useState } from 'react';
import { useSidebarStore } from '@/app/store/sidebarStore';
import styles from '@/app/styles/sideBar.module.css';
import { SessionInfoContainer } from '@/app/components/sidebar/SessionInfoContainer';
import { ModelSelectContainer } from '@/app/components/sidebar/ModelSelectContainer';
import { KeywordDescriptionContainer } from '@/app/components/sidebar/KeywordDescriptionContainer';
import { FaBars, FaChevronLeft, FaComments, FaCamera, FaKeyboard } from 'react-icons/fa';

export function SideBar() {
  const { isOpen, toggle, setIsOpen } = useSidebarStore();
  const sidebarRef = useRef<HTMLDivElement>(null);
  const [isMobile, setIsMobile] = useState<boolean>(false);


  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth <= 768;
      setIsMobile(mobile);
      // 창 크기 변경 시, 사이드바 상태를 강제 적용 (사용자의 조작 여부와 관계없이)
      if (mobile) {
        setIsOpen(false); // 모바일에서는 기본적으로 닫힘
      } else {
        setIsOpen(true); // 데스크톱에서는 기본적으로 열림
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [setIsOpen]); // isOpen을 의존성 배열에 추가

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isMobile && isOpen && sidebarRef.current && !sidebarRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isMobile && isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isMobile, isOpen]);

  return (
    <div className={styles.sidebarWrapper}>
      <div className={styles.miniSidebar}>
        <button className={styles.toggleButton} onClick={toggle} aria-label="Toggle Sidebar">
          {isOpen ? <FaChevronLeft size={20} /> : <FaBars size={20} />}
        </button>
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
      {/* 모바일에서 사이드바가 열려 있을 때 오버레이 추가 */}
      {isMobile && isOpen && <div className={styles.overlay} onClick={() => setIsOpen(false)}></div>}
      {/* 사이드바가 열려 있을 때만 전체 사이드바 보이기 */}
      <div 
        ref={sidebarRef} 
        className={`${styles.fullSidebarContent} ${isOpen ? '' : styles.hidden}`}
      >
        <SessionInfoContainer />
        <ModelSelectContainer />
        <KeywordDescriptionContainer />
      </div>
    </div>
  );
}
