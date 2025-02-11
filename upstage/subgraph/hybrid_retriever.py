import getpass
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.retrievers import BM25Retriever,EnsembleRetriever
from kiwipiepy import Kiwi
import cohere
# import dill

load_dotenv(override=True) # 강제 다시 로드

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

if not os.environ.get("PINECONE_API_KEY"):
  os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter Pinecone API key: ")

pinecone_api = os.environ["PINECONE_API_KEY"]
cohere_api = os.environ["COHERE_API_KEY"]

# vectorstore load
# 문서 검색 (Hybrid Search: BM25 + Pinecone)
# pinecone 벡터 기반 검색


pc = Pinecone(api_key=pinecone_api)

index_name = "sony"
index = pc.Index(index_name)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = PineconeVectorStore(embedding=embeddings, index=index)


retriever = vector_store.as_retriever(
  search_type="similarity", search_kwargs={"k": 10},
)

# BM25 키워드 기반 검색 
# ✅ BM25Retriever를 사용하여 키워드 기반 검색 수행
# ✅ 한국어 형태소 분석기 kiwipiepy를 사용하여 검색 성능 최적화
# ✅ BM25 모델을 .pkl 파일로 저장하여 로드 가능 -> drill로 로드
kiwi = Kiwi()
def kiwi_tokenize(text):
    return [token.form for token in kiwi.tokenize(text)]



# === 1. BM25Retriever와 Kiwi 로드 ===
with open("../data/zv-1.pkl", "rb") as f:
    bm25_retriever = dill.load(f)


bm25_retriever.preprocess_func = kiwi_tokenize

# === 3. Ensemble Retriever 생성 ===
# BM25 + Pinecone 결합 (Ensemble Search)
# 두 가지 검색 방식을 결합하여 검색 성능 향상 (하이브리드 검색)
ensemble_retriever = EnsembleRetriever(
    retrievers=[retriever, bm25_retriever],
    weights=[0.5, 0.5]  # Dense와 BM25 각각 50% 가중치
)

cohere_client = cohere.Client(cohere_api)