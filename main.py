import random
import logging
import uvicorn
import logging
from fastapi import FastAPI

# Configure logging
logging.basicConfig(
    filename = 'app.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("my_logger")
logger.info('Start Application!')

# Create application instance
app = FastAPI()

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
async def get_excuse():
    excuse = random.choice(excuses)
    logger.info({"excuse": excuse})
    return {"excuse": excuse}

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)