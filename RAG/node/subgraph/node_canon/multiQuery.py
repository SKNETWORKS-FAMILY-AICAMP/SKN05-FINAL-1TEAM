# multiquery.py
from node.subgraph.state import CanonState

from typing import List
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
import json

load_dotenv()

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
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    llm_chain = QUERY_PROMPT | llm | output_parser
    queries = llm_chain.invoke({"question":question})
    return queries

# graph node
def query_expansion(state: CanonState) -> CanonState:
    print("---[CANON] QUERY GENERTATE---")
    query = state["question"]
    transformed_queries = query_chain(query)
    return {"question":query, "transform_question": transformed_queries}