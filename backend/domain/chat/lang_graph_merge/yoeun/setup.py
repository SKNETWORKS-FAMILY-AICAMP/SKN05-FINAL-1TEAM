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

# def ensemble_retriever():
#     # return EnsembleRetriever(retrievers=[retriever, bm25_retriever], weights=[0.5, 0.5])
#     return EnsembleRetriever(retrievers=[retriever, bm25_retriever], weights=[0.5, 0.5])

def filter_embedding_model():
    # # filter model load
    local_model_dir = os.path.join(CURRENT_DIR, "models")  # 저장할 로컬 경로
    local_model_path = os.path.join(local_model_dir, "ko-sbert-sts")  # 저장할 로컬 경로

    if not os.path.exists(local_model_dir):
        os.makedirs(local_model_dir)

    # 모델 경로 설정
    model_name = "jhgan/ko-sbert-sts"  # 한국어 SBERT 임베딩 모델
    if not os.path.exists(local_model_path):
        model = SentenceTransformer(model_name)
        model.save(local_model_path)
    return SentenceTransformer(local_model_path)

def yoeun_cohere():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    cohere_api = os.environ["COHERE_API_KEY"]
    return cohere.Client(cohere_api)
