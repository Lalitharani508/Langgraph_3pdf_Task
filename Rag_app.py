from dotenv import load_dotenv
import os

load_dotenv()
from graph.graph import build_graph

app=build_graph()

def get_answer(question:str):
    result=app.invoke({"question": question})
    return result["answer"]