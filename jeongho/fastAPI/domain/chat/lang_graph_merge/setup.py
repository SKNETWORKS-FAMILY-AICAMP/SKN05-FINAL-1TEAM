import os
from dotenv import load_dotenv
from langchain_upstage import UpstageGroundednessCheck

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(CURRENT_DIR, ".env")

def UpsateGC():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    return UpstageGroundednessCheck()

def load_parent_dotenv():
    load_dotenv(dotenv_path=dotenv_path, override=True)

