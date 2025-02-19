from langchain_openai import ChatOpenAI
from langgraph.types import StreamWriter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from domain.chat.lang_graph_merge.hyeseo.state import SonyState
from domain.chat.lang_graph_merge.hyeseo.setup import load_hyeseo_dotenv


load_hyeseo_dotenv()


async def generate(state: SonyState, writer: StreamWriter):
    question = state["question"]
    context = state["rerank_context"]

    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    ANSWER_PROMPT = PromptTemplate(
        input_variables=["question","context"],
        template="""
    당신은 카메라 사용자 메뉴얼에 대한 정보를 제공하는 AI 어시스턴트입니다. 사용자가 질문을 하면, 제공된 Document 형식의 context를 활용하여 답변을 생성하세요. 각 Document에는 이미지 경로가 포함된 metadata가 있습니다. 답변을 생성할 때, 관련된 이미지가 있는 경우 ![image](metadata 내 이미지 경로) 형식으로 답변에 포함시켜 주세요. 

    예시:
    사용자 질문: "카메라의 ISO 설정 방법을 알려주세요."
    답변: "카메라의 ISO 설정은 메뉴에서 '설정'을 선택한 후 'ISO' 옵션을 선택하여 조정할 수 있습니다. ![image](/path/to/iso_setting_image)"

    이와 같은 형식으로 질문에 대한 답변을 생성하세요.
    이미지 경로가 없다면 이미지는 제외하고 답변을 생성하세요.

    컨텍스트와 질문을 기반으로 답변을 생성하세요:
    - 컨텍스트: {context}
    - 질문: {question}
    """
    )
    generation_chain = ANSWER_PROMPT | llm | StrOutputParser()

    chunks = []
    async for chunk in generation_chain.astream({"context": context, "question": question}):
        writer(
            {
                "currentNode": "답변 생성 중",
                "sessionId": state["sessionId"],
                "messageId": state["messageId"],
                "answer": chunk,
                "keywords": [],
                "suggestQuestions": []
            }
        )
        chunks.append(chunk)
    
    return {"question": question, "answer": "".join(chunks), "context":context}