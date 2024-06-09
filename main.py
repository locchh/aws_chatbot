import random
import uvicorn
from fastapi import FastAPI

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
    return {"message": "Welcome to the Funny Excuses API! Use /excuse to get a funny excuse."}

@app.get("/excuse")
def get_excuse():
    excuse = random.choice(excuses)
    return {"excuse": excuse}

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)