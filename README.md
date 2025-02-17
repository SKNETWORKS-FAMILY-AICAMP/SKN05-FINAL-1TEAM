# SKN05-FINAL-1TEAM 
**SKN 5기 최종 단위 프로젝트**
**프로젝트명:** 카메라 사용자 매뉴얼 검색 시스템  
**개발기간:** 2024.12.20 - 2025.02.19  

---

## 📍팀 소개 : CARAGSER📷
**김요은👩‍💻(팀장)** : 기획, 데이터 전처리, RAG 구현-캐논, 추가 RAG 모델 구현(키워드 추출, 추천질문 생성, Routing 등), 프론트엔드, 문서 작업<br>

**장정호👨‍💻**  : 기획, 데이터 전처리, RAG 구현-후지, 키워드 웹검색 모델 구현, 모델 전체 연결(Subgraph연결, 역질문 노드 등), 백엔드, 문서 작업<br>

**김혜서👩‍💻**  : 기획, 데이터 전처리, RAG 구현-소니, 프롬프트 엔지니어링, 백엔드, 문서 작업

---

### 📑프로젝트 개요
#### 주제 
LLM 활용 내부고객 업무 효율성 향상을 위한 문서 검색 시스템

#### 프로잭트 목표 
- 고객 상담 업무 효율성을 극대화 하기 위해 구매고객을 대상으로 서비스되고 있는 문서의 검색 시스템을 질의 응답(챗봇) 형식으로 구축
- 카메라 사용자의 카메라에 대한 정보 접근성 확대 및 초기 카메라 문제 발생 시 간편 해결 방안 제시로 편의성 증대

#### 프로젝트 기대 효과
- 이미지에 대한 처리 진행으로 검색 시 이미지가 답변에 함께 구현된다는 점에서 의의
- 카메라 시장에서만 활용하지 않고, 이미지가 있는 매뉴얼들의 시스템을 확장 가능성
- 사용자들에게 서비스 추가 제공을 통해 카메라 고객 응대의 퀄리티 증가

---

### 🛠 기술 스택
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langgraph&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Amazonaws](https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Next.js](https://img.shields.io/badge/Nextjs-000000?style=for-the-badge&logo=nextjs&logoColor=black)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)

![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)

---

### 🗓 WBS
<img src="./images/wbs.png">

---

### 📁시스템 구성도 / 시스템 아키텍쳐
<details>
<summary>시스템 구성도</summary>
   <img src="./images/System configuration.png">
   - 수집한 데이터<br>
    <img src="./images/data1.png"><br>
- 전처리<br>
    <img src="./images/data2.png"><br>
    <img src="./images/data3.png"><br>
    <img src="./images/data4.png"><br>
</details>
<details>
  <summary>시스템 아키텍쳐</summary>
    <img src="./images/system architecture.png">
</details>

---

### 화면설계서

---

### 🗂수행결과
<details>
<summary>📌 데이터 전처리</summary>

- **수집 데이터** : 카메라 사용자 매뉴얼  
  - 브랜드별 홈페이지에 업로드 되어있는 카메라 사용 매뉴얼 데이터  
  - **활용 브랜드** : 캐논, 소니, 후지필름  

- **파싱**  
  1. **텍스트 파싱**  
     - 사용 도구 : **Llama Parser, PyMuPDF**  
     - **문제점** : 텍스트와 혼용되는 이모티콘이 정상적으로 파싱되지 않음  
     - **해결 방법** : Llama Parser의 **MultiModal 모드**를 활용하여 LLM을 통해 파싱 데이터 수집  
  2. **이미지 파싱**  
     - 추출 방식 추가 예정  

- **청킹 (Chunking)**  
  - 데이터 전처리 단계에서 적용 예정  

</details>

<details>
<summary>캐논</summary>
    
   
</details>
<details>
<summary>소니</summary>
   
</details>
<details>
<summary>후지</summary>
    
 
</details>
<details>
<summary>전체 모델</summary>
    
   
</details>
<details>
<summary>결과/시연영상</summary>
    
 
</details>



