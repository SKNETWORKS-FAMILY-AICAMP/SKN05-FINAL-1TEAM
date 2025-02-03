# ingestion.py

import getpass
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import dill
from langchain.retrievers import EnsembleRetriever
from kiwipiepy import Kiwi
import cohere
from tokenizer import kiwi_tokenize
from sentence_transformers import SentenceTransformer

load_dotenv()

print("질문 환경 설정 중...")

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

if not os.environ.get("PINECONE_API_KEY"):
  os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter Pinecone API key: ")

pinecone_api = os.environ["PINECONE_API_KEY"]
cohere_api = os.environ["COHERE_API_KEY"]

# vectorstore load
pc = Pinecone(api_key=pinecone_api)

index_name = "canon"
index = pc.Index(index_name)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = PineconeVectorStore(embedding=embeddings, index=index)

retriever = vector_store.as_retriever(
  search_type="similarity", search_kwargs={"k": 10},
)

# reranker
cohere_client = cohere.Client(cohere_api)

# BM25Retriever와 Kiwi Load
with open("data/bm25_retriever_r50.pkl", "rb") as f:
    # bm25_retriever = pickle.load(f)
    bm25_retriever = dill.load(f)


bm25_retriever.preprocess_func = kiwi_tokenize

# Ensemble Retriever
ensemble_retriever = EnsembleRetriever(
    retrievers=[retriever, bm25_retriever],
    weights=[0.5, 0.5]  # Dense와 BM25 각각 50% 가중치
)

# filter model load
filter_embedding_model = SentenceTransformer("jhgan/ko-sbert-sts")

print("환경 설정 완료!")