import os
from openai import OpenAI
from temp_state import  RouterState

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_openai(input_data):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages= [
        {
            "role": "system",
            "content": '''너는 카메라 전문가다. 주어진 brand의 카메라에 대하여 설명하라. 한국어로 설명하라. 입력된 brand를 언급하라.
'''

        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f'''
brand: {input_data["brand"]}

Answer:
'''
                }
            ]
        }
    ]  ,
        temperature=0.0,
    )
    return response.choices[0].message.content


def generate_answer(state: RouterState) -> RouterState:
    input_data = {"brand": state["brand"]}
    results = ask_openai(input_data)
    return {"answer": results}


