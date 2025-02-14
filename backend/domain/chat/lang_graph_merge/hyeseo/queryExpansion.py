from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.hyeseo.state import OverallState, SonyState
from domain.chat.lang_graph_merge.hyeseo.setup import query_chain


def query_expansion(state: OverallState, writer: StreamWriter) -> SonyState:
    writer(
        {
            "currentNode": "문서 검색 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    writer(
        {
            "currentNode": "query_expansion(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    print("---[SONY] QUERY GENERTATE---")
    query = state["question"]
    transformed_queries = query_chain(query)
    print(query)
    print(transformed_queries)
    return {"question":query, "transform_question": transformed_queries}