import os
from langchain_community.adapters.openai import convert_openai_messages
from langchain_community.chat_models import ChatOpenAI
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_term(term):                                                 
    search_results = tavily_client.search(term, search_depth="basic")["results"] #  advanced
    return "\n".join([result["content"] for result in search_results[:3]])  # 상위 3개 결과를 반환

def explain_term(term):
    search_data = search_term(term)
    prompt = [
        {"role": "system", "content": "당신은 카메라 전문 용어를 쉽게 설명하는 전문가입니다."},
        {"role": "user", "content": f"다음 정보를 참고하여 간결한 설명을 작성하세요:\n\n"
                                    f"```\n{search_data}\n```\n\n"
                                    f"**설명 조건:**\n"
                                    f"- 사진 촬영과 카메라 기술과 관련된 정보만 사용\n"
                                    f"- 최대한 간결하게 \n"
                                    f"- 마크다운 문법 유지"}
    ]
    
    lc_messages = convert_openai_messages(prompt)
    explanation = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY")).invoke(lc_messages).content
    return explanation




