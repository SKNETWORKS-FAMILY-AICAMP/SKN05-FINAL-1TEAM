from langchain_upstage import UpstageGroundednessCheck
from openai import OpenAI

from state import OverallState


def relevance_check(state: OverallState):
    docs = state["context"]
    context = ""
    for i in docs:
        context += i.page_content
        context += "\n"
    answer = state["answer"]

    upstage_ground_checker = UpstageGroundednessCheck()
    request_input = {
    "context": context,
    "answer": answer,
    }
    relevance = upstage_ground_checker.invoke(request_input)
    print(relevance)
    return {"relevance" : relevance}
