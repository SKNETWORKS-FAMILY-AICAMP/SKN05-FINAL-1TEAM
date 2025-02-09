from domain.chat.lang_graph_merge.state import OverallState


def relevance_routing(state: OverallState):
    print(f"relevance_routing 확인 {state}")
    relevance = state.get("relevance","query_rewrite")
    if relevance == "grounded":
        return "keyword_extract"
    return "query_rewrite"