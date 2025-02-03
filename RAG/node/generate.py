# 답변 실행 역할

from typing import Any, Dict

from node.generation import generation_chain
from state import GraphState

def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    context = state["rerank_context"]

    generation = generation_chain.invoke({"context": context, "question": question})
    # print(f"question:{question}")
    # print(f"context:{context}")
    # print(f"generation:{generation}")
    
    message = [{"role": "user", "content": question},{"role":"assistant", "content":generation}]
    return {"question": question, "answer": generation, "message": message}