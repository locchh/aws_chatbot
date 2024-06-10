import os
os.environ['TOKENIZERS_PARALLELISM']= 'False'

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import random
import logging
import uvicorn
import logging
from fastapi import FastAPI

from openai import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# Configure logging
logging.basicConfig(
    filename = 'app.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("my_logger")
logger.info('Starting...')

# Create application instance
app = FastAPI()
logger.info('FastAPI Application Created!')

# Create embedding
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
logger.info('Embedding Created!')

# Load chromadb langchain
persist_directory = './chroma/'
loaded_vectordb = Chroma(
    persist_directory = persist_directory,
    embedding_function = embedding
)
logger.info('VectorDatabase Created!')

# load OPENAI_API_KEY
top_p = 1
temperature = 0.4
max_tokens = 150
model_name = 'gpt-3.5-turbo'

openai_api_key_path = '/home/loc/Documents/OPENAI_API_KEY.txt'
with open(openai_api_key_path) as f:
    OPENAI_API_KEY = f.read().strip()
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

client = OpenAI()
logger.info('OpenAI Client Created!')

# List of funny excuses
excuses = [
    "My dog ate my homework.",
    "I thought today was Saturday.",
    "I was abducted by aliens.",
    "My alarm didn't go off.",
    "I got stuck in the elevator.",
    "I lost my keys.",
    "I had to help a cat stuck in a tree.",
    "My goldfish is sick.",
    "I was too busy binge-watching my favorite show.",
    "My computer crashed and I lost all my work."
]

@app.get("/")
def read_root():
    logger.info({"message": "Welcome to the Funny Excuses API! Use /excuse to get a funny excuse."})
    return {"message": "Welcome to the Funny Excuses API! Use /excuse to get a funny excuse."}

@app.get("/excuse")
def get_excuse():
    excuse = random.choice(excuses)
    logger.info({"excuse": excuse})
    return {"excuse": excuse}

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)