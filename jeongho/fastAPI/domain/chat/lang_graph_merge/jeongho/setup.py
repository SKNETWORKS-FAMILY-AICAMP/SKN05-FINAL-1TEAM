import time
import os
import cohere
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from openai import OpenAI
from openai import AsyncOpenAI


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(CURRENT_DIR, ".env")

def load_jeongho_dotenv():
    load_dotenv(dotenv_path=dotenv_path, override=True)

def jeongho_client():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    return (OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

def jeongho_asyclient():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    return (AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")))

def jeongho_pinecone_index():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    spec = ServerlessSpec(cloud="aws", region="us-east-1")
    index_name = 'camera-document'
    # check if index already exists (it shouldn't if this is your first run)
    if index_name not in pc.list_indexes().names():
        # if does not exist, create index
        pc.create_index(
            index_name,
            dimension=1536,  # dimensionality of text-embed-3-small
            metric='dotproduct',
            spec=spec
        )
        # wait for index to be initialized
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
    # connect to index
    return (pc.Index(index_name))

def jeongho_cohere():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    return cohere.ClientV2()