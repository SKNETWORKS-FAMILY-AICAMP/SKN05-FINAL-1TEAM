from domain.chat.lang_graph_merge.state import OverallState


def relevance_routing(state: OverallState):
    relevance = state.get("relevance","query_rewrite")
    if relevance == "grounded":
        if state.get("brand") == "fuji":
            return ["translate_e2k\nonly_for_fuji"]
        else:
            return ["keyword_extract", "suggest_questions"]
    return ["query_rewrite"]