from dotenv import load_dotenv

load_dotenv()

from graph import app

if __name__ == "__main__":
    while True:
        question = input("질문을 입력하세요 (종료: 'exit') : ")
        
        if question.lower() == "exit":
            print("프로그램을 종료합니다.")
            break

        inputs = {"question": question}


        # app.stream() 실행 후 "generate" 노드인 경우만 출력
        for chunk_msg, metadata in app.stream(inputs, stream_mode="messages"):
            if metadata.get("langgraph_node") == "generate":
                print(chunk_msg.content, end="", flush=True)
        print("\n")