import nest_asyncio
import asyncio
import os
from openai import OpenAI
from state import GenerateState, OutputState

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_openai(input_data):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
    {
    "role": "system",
    "content": '''You are an AI assistant specializing in answer synthesis. Your task is to generate a single coherent response by analyzing multiple provided answers.

### Guidelines:
1. Identify and eliminate redundant or repetitive information.
2. Retain the most important and relevant details while ensuring logical flow.
3. Combine similar points concisely without losing meaning.
4. Ensure the response is well-structured, grammatically correct, and natural-sounding.
5. **Preserve all Markdown formatting**, including headings, lists, bold/italic text, and code blocks.
6. **Do not remove or alter Markdown image references (`![Image](file)`)** from the answers. They must be retained exactly as they appear.
7. If multiple answers contain the same image reference, include it only once in an appropriate location.
8. If any contradictions appear, resolve them based on majority consensus or the most reliable evidence.

Your final response must always follow **Markdown syntax**, preserving all relevant formatting and images.
'''
    }
,
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f'''
Question: {input_data["query"]}

Generate a single coherent response based on the following answers:
- Remove duplicate information.
- Retain important details while organizing them in a logical order.
- Construct a clear and natural sentence.

{''.join([f"[Answer {i+1}] {answer}\n" for i, answer in enumerate(input_data["answers"])])}
'''
            }
        ]
    }
]

  ,
        temperature=0.0,
    )
    return response.choices[0].message.content

def merge(state: GenerateState) -> OutputState:
    input_data = {}
    input_data["query"] = state["query"]
    input_data["answers"] = state["answers"]
    return { "temp": ask_openai(input_data)}





    results = asyncio.run(async_answer(state))
    print(results)
    return {
        "temp": results
    }  



