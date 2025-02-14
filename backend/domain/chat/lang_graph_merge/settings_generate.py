from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from domain.chat.lang_graph_merge.state import RouterState, OverallState

def settings_llm(question):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages= [
            {
                "role":"system",
                "content":"주어진 질문을 바탕으로 카메라의 설정에 대한 정보를 포함하여 답변을 작성하세요. 답변은 사용자가 이해하기 쉽게 명확하고 구체적으로 작성되어야 합니다. 사용자가 질문한 내용과 관련된 설정 정보를 반드시 제공하여, 사용자가 카메라를 더 잘 활용할 수 있도록 도와주세요."
            },
            {
                "role":"user",
                "content":f"{question}"
            },
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

def settings_question(question, answer):
    prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template="""
    당신은 카메라 사용자 메뉴얼에서 정보를 검색하여 사용자의 질문에 대한 답변을 제공하는 전문가입니다. 아래에 사용자의 질문과 LLM의 답변이 주어집니다. 이 정보를 바탕으로, 사용자가 카메라 사용자 메뉴얼에서 검색할 수 있는 구체적이고 명확한 질문을 생성하세요. 이 질문은 메뉴얼에서 관련 정보를 쉽게 찾을 수 있도록 설계되어야 합니다.

    1. **사용자 질문**: {question}
    2. **LLM의 답변**: {answer}

    위의 정보를 기반으로, 카메라 사용자 메뉴얼에서 검색할 수 있는 질문을 생성하세요. 이 질문은 사용자가 원하는 정보를 정확하게 찾을 수 있도록 돕는 것이 목적입니다.
    """
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    prompt_llm_chain = prompt | llm | StrOutputParser()
    result=prompt_llm_chain.invoke({'question':question,'answer':answer})
    return result

def settings_generate(state:RouterState) -> OverallState:
    question=state["question"]
    validation_results = state["validation_results"]
    
    setting_answer = settings_llm(question)
    result = settings_question(question, setting_answer)
    validation_results["is_setting"] = True

    return {
        **state,
        "ex_question": question,
        "question": result
    }