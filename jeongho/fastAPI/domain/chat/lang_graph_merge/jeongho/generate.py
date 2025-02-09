import os
import asyncio
import itertools
from glob import glob
from pydantic import BaseModel
from domain.chat.lang_graph_merge.jeongho.setup import jeongho_asyclient 
from domain.chat.lang_graph_merge.jeongho.state import RetrievalState, GenerateState

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(CURRENT_DIR, "image")

client = jeongho_asyclient()

async def ask_openai(input_data):
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages= [
        {
            "role": "system",
            "content": '''You are an AI assistant specializing in question-answering tasks. Your primary objective is to generate a well-structured and informative response based on the provided context.

### Guidelines:
1. **Use Markdown syntax in your response.** Ensure all formatting follows Markdown conventions, including headings, lists, bold/italic text, and code blocks where appropriate.
2. **Preserve all Markdown image references** (`![Image Description](file name)`) exactly as they appear in the provided context.
3. **Do not modify, remove, or interpret image references**. Keep them unchanged in your response.
4. **Do not generate new image references** beyond what is given in the context.
5. **Structure your response logically**, ensuring a natural flow of information while removing redundant content.
6. **If the context lacks sufficient information, respond with "I don't know" rather than making assumptions.**

Your responses must always be in **Markdown format** while maintaining the integrity of the provided content.
'''

        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f'''
Question: {input_data["query"]}

Context: 
Passage 1: 
{input_data["passages"][0]}
Metadata 1:
{input_data["metadata"][0]}
image path list 1:
{glob(os.path.join(image_dir, input_data["metadata"][0]['model'], "extracted_images",f"{input_data["metadata"][0]['model']}_page{input_data["metadata"][0]['page']}_*"))}

Passage 2: 
{input_data["passages"][1]}
Metadata 2:
{input_data["metadata"][1]}
image path list 2:
{glob(os.path.join(image_dir, input_data["metadata"][0]['model'], "extracted_images",f"{input_data["metadata"][0]['model']}_page{input_data["metadata"][0]['page']}_*"))}

Passage 3: 
{input_data["passages"][2]}
Metadata 3:
{input_data["metadata"][2]}
image path list 3:
{glob(os.path.join(image_dir, input_data["metadata"][0]['model'], "extracted_images",f"{input_data["metadata"][0]['model']}_page{input_data["metadata"][0]['page']}_*"))}

Answer:
'''
                }
            ]
        }
    ]  ,
        temperature=0.0,
    )
    return response.choices[0].message.content


class Passage(BaseModel):
    page_content: str

async def async_answer(state):
    tasks = []
    for i, query_from_QD in enumerate(state['query_decompose']):
        for j, query_from_MQE in enumerate(state["multi_query_expansion"][i]):
            input_data = {}
            input_data["query"] = query_from_MQE
            input_data["passages"] = state["rerank_passages"][i][j]
            input_data["metadata"] = state["rerank_passages_metadata"][i][j]
            tasks.append(ask_openai(input_data))
    results = await asyncio.gather(*tasks)
    return results

def generateAnswer(state: RetrievalState) -> GenerateState:
    results = asyncio.run(async_answer(state))

    # itertools를 사용하여 3차원 리스트를 1차원 리스트로 변환
    flattened_context = list(itertools.chain.from_iterable(itertools.chain.from_iterable(state["rerank_passages"])))
    context = [Passage(page_content=item) for item in flattened_context]
    print(f"generate노드\n{results}")
    return {
        "query": state["query"],
        "answers": results,
        "context": context
    }  