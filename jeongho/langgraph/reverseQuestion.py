from langgraph.types import interrupt
from temp_state import RouterState

def human_node(state: RouterState) -> RouterState:
    """Human node with validation."""
    question = "brand입력해라"

    while True:
        brand = interrupt(question)
        brand_list = ['fuji', "sony", "canon"]
        # Validate answer, if the answer isn't valid ask for input again.
        if not isinstance(brand, str) or brand not in  brand_list:
            question = f"'{brand} fuji, sony, canon만 검색 가능"
            brand = None
            continue
        else:
            # If the answer is valid, we can proceed.
            break

    print(f"{brand}를 입력 받음")
    return {
        "brand": brand
    }