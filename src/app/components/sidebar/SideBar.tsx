import styles from '@/app/styles/sideBar.module.css';
import { SessionInfoContainer } from '@/app/components/sidebar/SessionInfoContainer';
import { ModelSelectContainer } from '@/app/components/sidebar/ModelSelectContainer';
import { KeywordDescriptionContainer } from '@/app/components/sidebar/KeywordDescriptionContainer';

export function SideBar() {
  return (
    <div className={styles.sideBar}>
      <SessionInfoContainer />
      <ModelSelectContainer />
      <KeywordDescriptionContainer />
    </div>
  );
}