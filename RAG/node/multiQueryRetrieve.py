# multiQueryretrieve.py
from state import GraphState
from ingestion import retriever
from node.multiQuery import llm_chain

from langchain.retrievers.multi_query import MultiQueryRetriever

# Initialize the retriever
multiquery_retriever = MultiQueryRetriever(
    retriever=retriever, llm_chain=llm_chain, parser_key="lines"
)

# Node for retrieving documents
def multiquery_retrieve(state: GraphState) -> GraphState:
    print("---QUERY RETRIEVE---")
    transformed_queries = state["transform_question"]
    unique_docs = multiquery_retriever.invoke(transformed_queries)
    # print(unique_docs)
    return {"multi_context": unique_docs}