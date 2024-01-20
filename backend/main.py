import sys
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import os
import requests
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

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


@app.get("/check")
def check():
    return "Your API is up!"

