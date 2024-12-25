FROM ubuntu:24.04

RUN apt update

# git 설치
RUN apt install -y git 
# sudo 설치
RUN apt install -y sudo 

# 우분투 24.04버전에는 python 3.12가 설치
# 다른 특정 버전의 파이썬 설치시 deadsnakes PPA필요
RUN apt -y install python3

# pip 설치
RUN apt -y install python3-pip
# 패키지 설치 권한 해제
RUN python3 -m pip config set global.break-system-packages true
# pip 업그레이드 (기존 pip 버전 무시)
RUN pip install --upgrade --ignore-installed pip

# 라이브러리 설치
RUN pip install llama-index-core llama-parse llama-index-readers-file python-dotenv