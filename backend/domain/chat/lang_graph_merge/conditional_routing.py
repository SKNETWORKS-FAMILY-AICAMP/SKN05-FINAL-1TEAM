from domain.chat.lang_graph_merge.state import RouterState

def conditional_routing(state: RouterState):
    if state["next_step"] == "ask_brand":
        return "ask_brand"
    elif state["next_step"] == "not_for_camera":
        return "not_for_camera"
    elif state["next_step"] == "settings_generate":
        return "settings_generate"
    elif state["next_step"] == "rag_canon":
        return "rag_canon"
    elif state["next_step"] == "rag_sony":
        return "rag_sony"
    elif state["next_step"] == "rag_fuji":
        return "rag_fuji"
    elif state["next_step"] == "validate_input":
        return "validate_input"
    else:
        return "END"