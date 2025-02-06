# ingestion.py

import getpass
import os
import dill
from dotenv import load_dotenv

from kiwipiepy import Kiwi
from pinecone import Pinecone
from node.subgraph.tokenizer import kiwi_tokenize
from sentence_transformers import SentenceTransformer
import cohere

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.retrievers import EnsembleRetriever

load_dotenv()

print("질문 환경 설정 중...")

pinecone_api = os.environ["PINECONE_API_KEY"]
cohere_api = os.environ["COHERE_API_KEY"]

# vectorstore load
pc = Pinecone(api_key=pinecone_api)
index_name = "canon"
index = pc.Index(index_name)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

# retriever load
retriever = vector_store.as_retriever(
  search_type="similarity", search_kwargs={"k": 10},
)
with open("data/bm25_retriever.pkl", "rb") as f:
    bm25_retriever = dill.load(f)
bm25_retriever.preprocess_func = kiwi_tokenize

# Ensemble Retriever
ensemble_retriever = EnsembleRetriever(
    retrievers=[retriever, bm25_retriever],
    weights=[0.5, 0.5]
)

# reranker
cohere_client = cohere.Client(cohere_api)

# filter model load
filter_embedding_model = SentenceTransformer("jhgan/ko-sbert-sts")

print("환경 설정 완료!")