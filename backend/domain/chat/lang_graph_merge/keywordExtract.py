from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import OverallState
from domain.chat.lang_graph_merge.listChain import ListLLMChain

def keyword_extract(state: OverallState, writer: StreamWriter) -> Dict[str, Any]:
    writer(
        {
            "currentNode": "키워드 추출 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    print("---KEYWORD EXTRACT---")
    question = state["question"]
    context = state["context"]
    answer = state['answer']
    KEYWORD_PROMPT = PromptTemplate(
        input_variables=["question","context","answer"],
        template="""
        당신은 카메라 사용자 메뉴얼의 정보를 바탕으로 전문 용어를 추출하는 전문가입니다. 아래에 제공된 세 가지 정보를 기반으로 카메라와 관련된 전문 용어를 추출하세요. 출력은 리스트 형태로 제공해 주세요.

        1. **Context**: 카메라 사용자 메뉴얼에서 발췌한 정보입니다. 이 정보는 사용자가 질문한 내용에 대한 배경 지식을 제공합니다.
        2. **Question**: 사용자가 카메라에 대해 궁금해하는 질문입니다.
        3. **Answer**: 사용자의 질문에 대한 답변입니다.

        이 세 가지 정보를 종합하여 카메라와 관련된 전문 용어를 세 가지 추출하세요. 추출된 용어는 카메라의 기능, 설정, 부품, 기술적 사양 등을 포함할 수 있습니다. 예를 들어, '셔터 속도', '조리개', 'ISO 감도'와 같은 용어가 될 수 있습니다.

        **Context**: {context}

        **Question**: {question}

        **Answer**: {answer}

        **Output format: ["keyword1","keyword2","keyword3"]

        위의 정보를 바탕으로 카메라와 관련된 전문 용어를 추출하세요.
        """
        )

    chain = ListLLMChain()

    keywords = chain.run(KEYWORD_PROMPT, {"context": context, "question": question, "answer": answer})
    writer(
        {
            "currentNode": "키워드 추출 완료",
            "answer": "",
            "keywords": keywords,
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )

    return {"keyword" : keywords}