import React from 'react';
import styles from '@/app/styles/sideBar.module.css';



export function KeywordDescriptionContainer() {
  return (
    <div className={styles.container}>
      <h2 className={styles.containerTitle}>Keyword Description</h2>
      <p className={styles.descriptionText}>
        Select a camera model from the list to see its details here.
      </p>
    </div>
  );
}