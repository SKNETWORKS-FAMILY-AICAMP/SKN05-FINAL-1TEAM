from openai import AsyncOpenAI
from langgraph.types import StreamWriter
from domain.chat.lang_graph_merge.state import OverallState


# client = OpenAI()
client = AsyncOpenAI()

async def translate_e2k(state: OverallState, writer: StreamWriter):

    writer(
        {
            "currentNode": "translate_e2k(확인을 위한 출력)",
            "answer": "",
            "keywords": [],
            "suggestQuestions": [],
            "sessionId": state.get("sessionId"),
            "messageId": state.get("messageId"),
        }
    )

    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                            {
                            "type": "text",
                            "text": "You are a professional camera manual translator. Your goal is to translate any provided English text—specifically content generated via a RAG system about camera manuals—into Korean. Please preserve the original Markdown formatting while ensuring your translation remains accurate, clear, and natural in Korean. Maintain a formal and precise tone befitting a technical document, and do not alter the original structure or meaning."
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                    {
                    "type": "text",
                    "text": state["answer"]
                    }
                ]
            }
        ],
        stream=True,
    )

    chunks = []
    current_node = "답변 생성 중"
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            writer(
                {
                    "currentNode": current_node,
                    # "sessionId": state["sessionId"],
                    # "messageId": state["messageId"],
                    "answer": chunk.choices[0].delta.content,
                    "keywords": [],
                    "suggestQuestions": []
                }
            )
            chunks.append(chunk.choices[0].delta.content)
        else:
            pass
            # writer(
            #     {
            #         "currentNode": current_node,
            #         # "sessionId": state["sessionId"],
            #         # "messageId": state["messageId"],
            #         "answer": "",
            #         "keywords": ["temp keyword 1", "temp keyword 2", "temp keyword 3"],
            #         "suggestQuestions": ["temp suggestQuestion 1", "temp suggestQuestion 2", "temp suggestQuestion 3"]
            #     }
            # )
    return {"answer": "".join(chunks)}