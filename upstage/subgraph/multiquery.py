from typing import List
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
import json

load_dotenv()

# 🔹 output 정의
class LineListOutputParser(BaseOutputParser[List[str]]):
    """
    LLM 응답을 리스트로 변환하는 Output Parser.
    """
    def parse(self, text: str) -> List[str]:
        if isinstance(text, AIMessage):
            text = text.content  # AIMessage 객체에서 content 추출
        
        try:
            parsed_json = json.loads(text)
            return parsed_json  # JSON 리스트 반환
        except json.JSONDecodeError:
            lines = text.strip().split("\n")
            return list(filter(None, lines))  # 빈 줄 제거 후 리스트 반환

# Output Parser 인스턴스 생성
output_parser = LineListOutputParser()

# 🔹 Query Prompt 정의
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions in a JSON array format, separated by commas.
    Do not include any additional explanations.
    Original question: {question}
    Output format: ["question1", "question2", "question3", "question4", "question5"]""",
)

# 🔹 LLM 모델 설정
llm = ChatOpenAI(temperature=0, model="gpt-4o") 

# 🔹 LLM Chain 생성
llm_chain = QUERY_PROMPT | llm | output_parser


# 🔹 GraphState 기반 변형 쿼리 생성 함수
def generate_transformed_queries(state: "GraphState") -> "GraphState":
    """
    원본 질문을 기반으로 변형된 다섯 개의 질문을 생성하여 GraphState에 추가합니다.
    """
    print("--- QUERY GENERATION STARTED ---")
    
    query = state["question_state"]["question"]  # 원본 질문 가져오기
    transformed_queries = llm_chain.invoke({"question": query})  # LLM 호출

    print(f"Generated Queries: {transformed_queries}")

    # State 업데이트
    state["question_state"]["transform_question"] = transformed_queries
    return state
