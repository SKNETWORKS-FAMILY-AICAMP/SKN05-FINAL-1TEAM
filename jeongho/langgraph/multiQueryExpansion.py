import os
import pandas as pd
from state import RetrievalState
from autorag.nodes.queryexpansion.multi_query_expansion import MultiQueryExpansion

generator_dict = {
    "generator_module_type": "llama_index_llm",
    "llm": "openai",
    "model": "gpt-4o",
    # 기타 필요한 파라미터...
}

project_dir = "./autorag/project_dir"
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

mqe = MultiQueryExpansion(
    project_dir=project_dir,
    **generator_dict
)

def multiQueryExpansion(state: RetrievalState) -> RetrievalState:
    df_input = pd.DataFrame(
        {
            "query": state["query_decompose"]
        }
    )
    MQE_result_df = mqe.pure(previous_result=df_input)
    return {"multi_query_expansion": list(MQE_result_df["queries"])}
