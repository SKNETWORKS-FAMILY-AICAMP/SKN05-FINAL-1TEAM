import os
import json
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser

import os
import dill
import cohere
from dotenv import load_dotenv
from pinecone import Pinecone
from kiwipiepy import Kiwi
from sentence_transformers import SentenceTransformer
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.retrievers import EnsembleRetriever

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(CURRENT_DIR, ".env")

def load_hyeseo_dotenv():
    load_dotenv(dotenv_path=dotenv_path, override=True)


def kiwi_tokenize(text):
    kiwi = Kiwi()
    return [token.form for token in kiwi.tokenize(text)]


def ensemble_retriever():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    pinecone_api = os.environ["PINECONE_API_KEY"]
    pc = Pinecone(api_key=pinecone_api)
    index_name = "sony"
    index = pc.Index(index_name)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = PineconeVectorStore(embedding=embeddings, index=index)
    # retriever load
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 10},
    )
    # pkl_path = os.path.join(CURRENT_DIR, "data", "bm25_retriever_a6400.pkl")
    # with open(pkl_path, "rb") as f:
    #     bm25_retriever = dill.load(f)
    # bm25_retriever.preprocess_func = kiwi_tokenize
    return EnsembleRetriever(retrievers=[retriever], weights=[1])
    # return EnsembleRetriever(retrievers=[retriever, bm25_retriever], weights=[0.5, 0.5])

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

def query_chain(question):
    load_dotenv(dotenv_path=dotenv_path, override=True)
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

def hyeseo_cohere():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    cohere_api = os.environ["COHERE_API_KEY"]
    return cohere.Client(cohere_api)