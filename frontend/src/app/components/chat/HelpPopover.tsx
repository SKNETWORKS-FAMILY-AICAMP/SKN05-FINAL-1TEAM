import React from 'react';
import styles from '@/app/styles/chat.module.css';

interface HelpPopoverProps {
  onClose: () => void;
}

export default function HelpPopover({ onClose }: HelpPopoverProps) {
  return (
    <div className={styles.helpPopover}>
      <div className={styles.helpContent}>
        <div className={styles.helpHeader}>
          <h3>Info Guide</h3>
          <button 
            onClick={onClose}
            className={styles.closeButton}
            aria-label="닫기"
          >
            ×
          </button>
        </div>
        <div className={styles.helpSection}>
          {/* <h4>단축키</h4> */}
          <ul>
            <li>1. 본 시스템은 카메라 사용자 메뉴얼을 토대로 답변하는 시스템 입니다. </li>
            <li>2. 카메라의 브랜드를 질문에 포함하면 더 정확한 답변을 얻을 수 있습니다.</li>
            <li>3. 카메라 설정과 관련된 질문에 심도있게 답변합니다.</li>
          </ul>
        </div>
      </div>
    </div>
  );
} 