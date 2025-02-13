import React from 'react';
import styles from '@/app/styles/chat.module.css';

interface ProgressStepProps {
  currentNodes: string[];
  isGenerating?: boolean;
}

export function ProgressStep({ 
  currentNodes, 
  isGenerating = false 
}: ProgressStepProps) {
  // END 노드 체크
  const isEnd = currentNodes.length > 0 && currentNodes[currentNodes.length - 1] === "END";
  
  if (isEnd) return null;

  return (
    <div className={styles.currentNodeMessage}>
      <div className={styles.currentNodeContainer}>
        <div className={styles.currentNodes}>
          {currentNodes.map((node, index) => (
            <div key={index} className={styles.currentNode}>
              <div 
                className={
                  index < currentNodes.length - 1 
                    ? styles.successMark 
                    : styles.loadingSpinner
                }
              >
                {index < currentNodes.length - 1 ? "✔️" : ""}
              </div>
              {node}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}