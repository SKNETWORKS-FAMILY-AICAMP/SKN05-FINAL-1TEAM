from state import OverallState
from openai import OpenAI

def query_rewrite(state: OverallState):
    question = state["question"]
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages= [
            {
                "role":"system",
                "content":"당신은 카메라 사용자 메뉴얼에 대한 질문을 재작성하는 전문가입니다. 사용자가 제공한 질문이 명확하지 않거나 시스템에 적합하지 않을 수 있습니다. 주어진 질문을 바탕으로, 카메라 사용자 메뉴얼에서 답변을 찾을 수 있도록 명확하고 구체적인 질문으로 재작성하세요. 재작성된 질문만 답변하세요."
            },
            {
                "role":"user",
                "content":f"{question}"
            },
        ],
        temperature=0.0,
    )

    new_query = response.choices[0].message.content

    return { "question": new_query }