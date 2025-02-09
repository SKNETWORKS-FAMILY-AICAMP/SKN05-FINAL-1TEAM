import os
import pandas as pd
from state import InputState, RetrievalState
from autorag.nodes.queryexpansion.query_decompose import QueryDecompose

generator_dict = {
    "generator_module_type": "llama_index_llm",  # 예) 이 이름에 해당하는 클래스를 get_support_modules가 로드
    "llm": "openai",        # 예시: openai
    "model": "gpt-4o", # 예시: gpt-4o-mini
    # 기타 필요한 파라미터...
}

project_dir = "./autorag/project_dir"
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

decomposer = QueryDecompose(
    project_dir=project_dir,
    **generator_dict  # -> make_generator_callable_param() 호출로 실제 Generator 인스턴스 생성
)

def queryDecompose(state: InputState) -> RetrievalState:
    df_input = pd.DataFrame(
        {
            "query": [
                state.question
            ]
        }
    )
    QD_result_df = decomposer.pure(previous_result=df_input)
    return {
        "query": state.question,
        "query_decompose": QD_result_df["queries"][0]
    }       
        
        
        
        
