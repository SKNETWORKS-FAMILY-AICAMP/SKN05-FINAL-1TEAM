from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.jeongho.setup import jeongho_asyclient
from domain.chat.lang_graph_merge.jeongho.state import GenerateState
from domain.chat.lang_graph_merge.state import OverallState


client = jeongho_asyclient()
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
        stream=True
    )
    return response

async def merge(state: GenerateState, writer: StreamWriter) -> OverallState:
    input_data = {}
    input_data["query"] = state["query"]
    input_data["answers"] = state["answers"]
    stream = await ask_openai(input_data)

    chunks = []
    current_node = "generate"
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            writer(
                {
                    "currentNode": current_node,
                    "sessionId": state["sessionId"],
                    "messageId": state["messageId"],
                    "answer": chunk.choices[0].delta.content,
                    "keywords": [],
                    "suggestQuestions": []
                }
            )
            chunks.append(chunk.choices[0].delta.content)
        else:
            writer(
                {
                    "currentNode": current_node,
                    "sessionId": state["sessionId"],
                    "messageId": state["messageId"],
                    "answer": "",
                    "keywords": [],
                    "suggestQuestions": []
                }
            )
    return {
        "context": state["context"],
        "answer": "".join(chunks)
        }





    # answer_merge = ask_openai(input_data)
    # print(f"merge노드\n{answer_merge}")
    # return {
    #     "context": state["context"],
    #     "answer": answer_merge
    #     }








