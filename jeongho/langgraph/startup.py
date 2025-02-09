from dotenv import load_dotenv
import nest_asyncio

import time
import os
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

load_dotenv(dotenv_path=".env", override=True)
nest_asyncio.apply()

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
index = pc.Index(index_name)
time.sleep(1)
# view index stats
# index.describe_index_stats()
def pincone_index():
    return index