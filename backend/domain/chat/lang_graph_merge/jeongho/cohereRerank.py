import os
import pandas as pd
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.jeongho.state import RetrievalState
from domain.chat.lang_graph_merge.jeongho.setup import jeongho_cohere


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
corpus_path = os.path.join(CURRENT_DIR, "autorag/project_dir/data/corpus.parquet")
corpus_df = pd.read_parquet(corpus_path)

for i in range(len(corpus_df)):
    corpus_df["metadata"][i]["subsection"] = list(corpus_df["metadata"][i]["subsection"])
    
co = jeongho_cohere()

def cohereRerank(state: RetrievalState, writer: StreamWriter) -> RetrievalState:
    writer(
        {
            "currentNode": "문서 정렬 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )

    rerank_passages = []
    rerank_passages_metadata = []
    for i, _ in enumerate(state["query_decompose"]):
        rerank_passages_QD = []
        rerank_passages_QD_metadata = []
        for j, query_from_MQE in enumerate(state["multi_query_expansion"][i]):
            docs = []
            docs_metadata = []
            for id in state["hybrid_cc_IDs"][i][j]:
                docs.append(corpus_df.loc[corpus_df["doc_id"] == id, "contents"].values[0])
                docs_metadata.append(corpus_df.loc[corpus_df["doc_id"] == id, "metadata"].values[0])
                
            response = co.rerank(
                model="rerank-v3.5",
                query=query_from_MQE,
                documents=docs,
                top_n=3,
            )
            rerank_passages_MQE = []
            rerank_passages_MQE_metadata = []
            for k in response.dict()['results']: 
                rerank_passages_MQE.append(docs[k['index']])
                rerank_passages_MQE_metadata.append(docs_metadata[k['index']])
            rerank_passages_QD.append(rerank_passages_MQE)
            rerank_passages_QD_metadata.append(rerank_passages_MQE_metadata)
        rerank_passages.append(rerank_passages_QD)
        rerank_passages_metadata.append(rerank_passages_QD_metadata)
    return {"rerank_passages": rerank_passages, "rerank_passages_metadata": rerank_passages_metadata}