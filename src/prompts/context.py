import os
import re
import pdfplumber
import openai
from pinecone import Pinecone, PodSpec
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
MODEL = "text-embedding-ada-002"



# initialize connection to pinecone
api_key = os.getenv('PINECONE_API_KEY')
# configure client
pc = Pinecone(api_key=api_key)

import time

index_name = '10-academy'
existing_indexes = [
    index_info["name"] for index_info in pc.list_indexes()
]

# check if index already exists (it shouldn't if this is first time)
if index_name not in existing_indexes:
    try:
        # if does not exist, create index
        pc.create_index(
            index_name,
            dimension=1536,  # dimensionality of ada 002
            metric='dotproduct',
            spec=PodSpec(
                environment="gcp-starter"
            ) 
        )
        # wait for index to be initialized
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
    except Exception as e:
        print(f"Failed to create index: {e}")
        # Handle the error appropriately here

# connect to index
index = pc.Index(index_name)
time.sleep(1)
# view index stats
index.describe_index_stats()

# Define a function to preprocess text
def preprocess_text(text):
    # Replace consecutive spaces, newlines and tabs
    text = re.sub(r'\s+', ' ', text)
    return text

def process_pdf(file_path):
    # create a loader
    loader = PyPDFLoader(file_path)
    # load your data
    data = loader.load()
    # Split your data up into smaller documents with Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(data)
    # Convert Document objects into strings
    texts = [str(doc) for doc in documents]
    return texts

# Define a function to create embeddings
def create_embeddings(texts):
    embeddings_list = []
    for text in texts:
        res = openai.Embedding.create(input=[text], engine=MODEL)
        embeddings_list.append(res['data'][0]['embedding'])
    return embeddings_list

# Define a function to upsert embeddings to Pinecone
def upsert_embeddings_to_pinecone(index, embeddings, ids):
    index.upsert(vectors=[(id, embedding) for id, embedding in zip(ids, embeddings)])

# Process a PDF and create embeddings
file_path = "10_Academy_challenge_doc.pdf"
texts = process_pdf(file_path)
embeddings = create_embeddings(texts)

# Upsert the embeddings to Pinecone
upsert_embeddings_to_pinecone(index, embeddings, [file_path])