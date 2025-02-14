import styles from "@/app/styles/chat.module.css";

export function CurrentNodes({ currentNodes }: { currentNodes: string[] }) {
  const isEnd = currentNodes.length > 0 && currentNodes[currentNodes.length - 1] === "END";

  // isEnd가 true이면 아무것도 렌더링하지 않음
  if (isEnd) return null;

  return (
    <div className={styles.currentNodeContainer}>
      <div className={styles.currentNodes}>
        {currentNodes.map((currentNode, index) => (
          <div key={index} className={styles.currentNode}>
            <div className={index < currentNodes.length - 1 ? styles.successMark : styles.loadingSpinner}>
              {index < currentNodes.length - 1 ? "여기✔️있어요" : ""}
            </div>
            {currentNode}
          </div>
        ))}
      </div>
    </div>
  );
}
