import styles from "@/app/styles/chat.module.css";

export function CurrentNodes({ currentNodes }: { currentNodes: string[] }) {
  const isEnd = currentNodes.length > 0 && currentNodes[currentNodes.length - 1] === "END";
  const isRQ = currentNodes.length > 0 && currentNodes[currentNodes.length - 1] === "refine_question";

  return (
    <div className={styles.currentNodeContainer}>
      <div className={styles.currentNodes}>
        {currentNodes
          .slice(0, isEnd || isRQ ? currentNodes.length - 1 : currentNodes.length) // ✅ 마지막 요소 제외 조건 적용
          .map((currentNode, index) => (
            <div key={index} className={styles.currentNode}>
              <div className={isEnd || isRQ || index < currentNodes.length - 1 ? styles.successMark : styles.loadingSpinner}>
                {(isEnd || isRQ || index < currentNodes.length - 1) ? "✔️" : ""}
              </div>
              {currentNode}
            </div>
          ))}
      </div>
    </div>
  );  
}
