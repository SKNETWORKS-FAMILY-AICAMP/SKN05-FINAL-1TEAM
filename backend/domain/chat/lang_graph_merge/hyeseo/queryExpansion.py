from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.state import OverallState
from domain.chat.lang_graph_merge.hyeseo.setup import query_chain


def query_expansion(state: OverallState, writer: StreamWriter) -> SonyState:
    print("---SONY---")
    query = state["question"]
    transformed_queries = query_chain(query)
    return {"question":query, "transform_question": transformed_queries}