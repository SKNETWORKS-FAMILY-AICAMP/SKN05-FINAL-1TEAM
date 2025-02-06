import json
from langchain_core.output_parsers import BaseOutputParser
from typing import List, Any, Dict
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# listLLM class
class ListOutputParser(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        if isinstance(text, AIMessage):
            text = text.content
        
        try:
            parsed_json = json.loads(text)
            return parsed_json
        except:
            lines = text.replace("[","").replace("]","").strip().split(",")
            return list(filter(None, lines))

class ListLLMChain:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0):
        self.llm = ChatOpenAI(temperature=temperature, model=model_name)
        self.parser = ListOutputParser()
    
    def create_chain(self, prompt: PromptTemplate):
        return prompt | self.llm | self.parser
    
    def run(self, prompt: PromptTemplate, inputs: Dict[str, Any]) -> List[str]:
        chain = self.create_chain(prompt)
        return chain.invoke(inputs)
