from dotenv import load_dotenv
import uuid
load_dotenv()

from graph import app


if __name__ == "__main__":
    while True:
        question = input("질문을 입력하세요 (종료: 'exit') : ")
        
        if question.lower() == "exit":
            print("프로그램을 종료합니다.")
            break

        random_uuid_hex = uuid.uuid4().hex
        thread = {"configurable": {"thread_id": random_uuid_hex}}
        inputs = {"question": question, "brand":"canon"}


        # app.stream() 실행 후 "generate" 노드인 경우만 출력
        # for chunk_msg, metadata in app.stream(inputs, config=thread, stream_mode="updates", subgraphs=True):
        #     if metadata.get("langgraph_node") == "generate":
        #         print(chunk_msg.content, end="", flush=True)
        # print("\n")
        
        for event in app.stream(inputs, config=thread, stream_mode="updates", subgraphs=True):
            print(event)
            print("\n")