import styles from '@/app/styles/chat.module.css';
import { CurrentNodes } from './CurrentNodes';

interface CurrentNodeMessageProps {
  currentNodes: string[];
  isGenerating?: boolean;
}

export function CurrentNodeMessage({ 
  currentNodes, 
  isGenerating = false
}: CurrentNodeMessageProps) {
  return (
    <div className={styles.currentNodeMessage}>
        <CurrentNodes 
            currentNodes={currentNodes}
          />
    </div>
  );
}
