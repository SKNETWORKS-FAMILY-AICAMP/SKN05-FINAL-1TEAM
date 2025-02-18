import os
import dill
import json
import cohere
from dotenv import load_dotenv
from pinecone import Pinecone
from kiwipiepy import Kiwi
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(CURRENT_DIR, ".env")

def load_yoeun_dotenv():
    load_dotenv(dotenv_path=dotenv_path, override=True)

def kiwi_tokenize(text):
    kiwi = Kiwi()
    return [token.form for token in kiwi.tokenize(text)]

load_dotenv(dotenv_path=dotenv_path, override=True)
pinecone_api = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=pinecone_api)
index_name = "canonmodel"
index = pc.Index(index_name)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)
# retriever load
retriever = vector_store.as_retriever(
    search_type="similarity", search_kwargs={"k": 10}, 
)
pkl_path = os.path.join(CURRENT_DIR, "data", "bm25_retriever.pkl")
with open(pkl_path, "rb") as f:
    bm25_retriever = dill.load(f)
bm25_retriever.preprocess_func = kiwi_tokenize

embedding_path = os.path.join(CURRENT_DIR, "data", "combined_embeddings.json")
with open(embedding_path, "r", encoding="utf-8") as f:
    embedding_data = json.load(f)



def yoeun_cohere():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    cohere_api = os.environ["COHERE_API_KEY"]
    return cohere.Client(cohere_api)
