import styles from '@/app/styles/sideBar.module.css';

export function SessionInfoContainer() {
  return (
    <div className={styles.container}>
      <h2 className={styles.containerTitle}>User Info & Chat Sessions</h2>
      <div className={styles.infoBox}>
        <p><strong>User:</strong> John Doe</p>
        <p><strong>Session:</strong> Active Chat</p>
      </div>
    </div>
  );
}