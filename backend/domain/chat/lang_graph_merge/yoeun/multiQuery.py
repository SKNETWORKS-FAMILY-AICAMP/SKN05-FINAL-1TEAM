# multiquery.py
import json
from typing import List
from langgraph.types import StreamWriter
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from domain.chat.lang_graph_merge.yoeun.state import CanonState
from domain.chat.lang_graph_merge.yoeun.setup import load_yoeun_dotenv

load_yoeun_dotenv()

# output 정의
class LineListOutputParser(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        if isinstance(text, AIMessage):
            text = text.content
        
        try:
            parsed_json = json.loads(text)
            return parsed_json
        except:
            lines = text.strip().split("\n")
            return list(filter(None, lines))

output_parser = LineListOutputParser()


def query_chain(question):
    output_parser = LineListOutputParser()
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
    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    llm_chain = QUERY_PROMPT | llm | output_parser
    queries = llm_chain.invoke({"question":question})
    return queries

# graph node
def query_expansion(state: CanonState, writer: StreamWriter) -> CanonState:
    writer(
        {
            "currentNode": "문서 검색 중",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )
    print("---[CANON] QUERY GENERTATE---")
    query = state["question"]
    model = state.get("model")
    print(f"qustion : {query}, model: {model}")


    transformed_queries = query_chain(query)
    print(transformed_queries)
    return {"question":query, "model":model, "transform_question": transformed_queries}