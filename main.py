import os
os.environ['TOKENIZERS_PARALLELISM']= 'False'

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import random
import logging
import uvicorn
import logging

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

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
logger.info('Start Initialization!')

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

# Create client OpenAI
client = OpenAI()
logger.info('OpenAI Client Created!')

# Create application instance
app = FastAPI()
logger.info('FastAPI Application Created!')

logger.info('Initialization Successful!')

class OpenAIRequest(BaseModel):
    prompt: str
    max_tokens: int = max_tokens

class QuestionRequest(BaseModel):
    prompt: str

@app.get("/")
async def get_ui():
    html_content = """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Chat UI</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

            body {
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(135deg, #f0f0f0 25%, #dcdcdc 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                width: 400px;
                text-align: center;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            .container:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
            }

            h1 {
                font-size: 28px;
                margin-bottom: 20px;
                color: #333;
            }

            textarea, input {
                width: calc(100% - 24px);
                padding: 12px;
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.2s;
            }

            textarea:focus, input:focus {
                border-color: #007bff;
            }

            button {
                width: 100%;
                padding: 12px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 500;
                transition: background-color 0.2s, transform 0.2s;
            }

            button:hover {
                background-color: #0056b3;
                transform: translateY(-2px);
            }

            #response {
                margin-top: 20px;
                font-size: 16px;
                color: #333;
                word-wrap: break-word;
                text-align: left;
                background-color: #f9f9f9;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
        </style>
    </head>

    <body>

        <div class="container">
            <h1>AWS ChatBot</h1>
            <textarea id="prompt" rows="4" placeholder="Enter your prompt here..."></textarea><br>
            <input type="number" id="max_tokens" value="50" min="1" max="150"><br>
            <button onclick="generateQuestion()">Ask Question</button>
            <p id="response"></p>
        </div>

        <script>
            async function generateQuestion() {
                const prompt = document.getElementById("prompt").value;
                const max_tokens = document.getElementById("max_tokens").value;

                const response = await fetch('/question', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt: prompt, max_tokens: parseInt(max_tokens) })
                });
                const data = await response.json();
                document.getElementById("response").innerText = data.text;
            }
        </script>

    </body>

    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

@app.post('/question')
async def generate_question(request: QuestionRequest):
    try:
        questions = loaded_vectordb.similarity_search(request.prompt,k=5)
        question = random.choice(questions)

        logger.info(
            {'role': 'user',
            'content': request.prompt,
            'status': 200,
            'text': question.page_content
            })

        return {'text':question.page_content}
    except Exception as e:
        logger.info(
            {'role': 'user',
            'content': request.prompt,
            'status': 500,
            'text': str(e)
            })

        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_text(request: OpenAIRequest):
    try:
        response = client.chat.completions.create(
            model = model_name,
            messages = [{'role':'user','content':request.prompt}],
            max_tokens = request.max_tokens,
            temperature = temperature,
            top_p = top_p
            )

        logger.info(
            {'role': 'user',
            'content': request.prompt,
            'status': 200,
            'text': response.choices[0].message.content
            })

        return {'text':response.choices[0].message.content}
    except Exception as e:

        logger.info(
            {'role': 'user',
            'content': request.prompt,
            'status': 500,
            'text': str(e)
            })

        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)