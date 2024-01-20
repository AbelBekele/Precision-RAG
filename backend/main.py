import sys
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import os
import requests
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from evaluation._prompt_generation import PromptGenerator
from evaluation._evaluation import Evaluator
from utility.env_manager import get_env_manager
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    num_test_output: str
    objective: str
    output: str

class EvaluationItem(BaseModel):
    query: str
    user_message: str

@app.get("/check")
def check():
    return "Your API is up!"

@app.post("/generate")
def generate(item: Item):
    env_manager = get_env_manager()
    client = OpenAI(api_key=env_manager['openai_keys']['OPENAI_API_KEY'])
    generator = PromptGenerator(item.num_test_output, item.objective, item.output)
    with open('prompt-dataset/prompt-data.json', 'r') as f:
        prompts = json.load(f)

    top_score = -1
    top_result = None

    # Iterate through each prompt
    for prompt in prompts:
        # Create an EvaluationItem from the prompt
        evaluation_item = EvaluationItem(query=item.objective, user_message=prompt['Prompt'])

        # Run the evaluation
        evaluator = Evaluator(env_manager, client)
        evaluation_result, accuracy, sufficient = evaluator.run(evaluation_item.query, evaluation_item.user_message)

        # Set check_classification to True
        sufficient = "true"

        # If the accuracy of this result is higher than the current top score and sufficient is True, update the top score and result
        if sufficient == "true" and accuracy > top_score:
            top_score = accuracy
            top_result = {"prompt": prompt['Prompt'], "score": f"{top_score}%"}

        return top_result
        
@app.post("/evaluate")
def evaluate(item: EvaluationItem):
    evaluator = Evaluator(env_manager, client)
    result = evaluator.run(item.query, item.user_message)
    return {"result": result}