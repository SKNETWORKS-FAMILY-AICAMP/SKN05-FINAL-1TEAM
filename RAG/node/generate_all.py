# 서브 그래프를 및 라우팅 테스트를 위한 임시파일
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from state import OverallState

def generate_all_chain(question):
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    ANSWER_PROMPT = PromptTemplate(
        input_variables=["question","context"],
        template="""
    당신은 카메라에 대한 정보를 제공하는 AI 어시스턴트입니다. 사용자가 질문을 하면, 답변을 생성하세요. 

    예시:
    사용자 질문: "카메라의 ISO 설정 방법을 알려주세요."
    답변: "카메라의 ISO 설정은 메뉴에서 '설정'을 선택한 후 'ISO' 옵션을 선택하여 조정할 수 있습니다. 

    이와 같은 형식으로 질문에 대한 답변을 생성하세요.

    질문을 기반으로 답변을 생성하세요:
    - 질문: {question}
    """
    )
    generation_chain = ANSWER_PROMPT | llm | StrOutputParser()
    answer = generation_chain.invoke({"question":question})
    return answer

def generate_all(state: OverallState):
    print("---GENERATE---")
    question = state["question"]

    # context = state["rerank_context"]
    result = generate_all_chain(question)
    
    return {"question": question, "answer": result}