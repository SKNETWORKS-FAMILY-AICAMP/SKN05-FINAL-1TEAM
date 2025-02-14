from domain.chat.lang_graph_merge.jeongho.state import InputState
from domain.chat.lang_graph_merge.jeongho.setup import jeongho_client


client = jeongho_client()
def translate_k2e(state: InputState) -> InputState:
    messages=[
    {
      "role": "system",
      "content": "You are a professional translator specializing in converting Korean text into English. Your primary goal is to translate the given Korean input into English with absolute accuracy, preserving its original structure. Do not interpret, rephrase, or add any explanations—just provide the direct translation."
    },
    {
      "role": "user",
      "content": f'''Korean text: {state.question}
English text: '''
    }
  ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages= messages,
        temperature=0.0,
    )
    
    question = response.choices[0].message.content    
    print(f"translate_k2e노드: {question}")
    return { "question": question }