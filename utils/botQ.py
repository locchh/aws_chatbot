import os
import random
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# Create embedding
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Load chromadb langchain
persist_directory = './chroma/'
loaded_vectordb = Chroma(
    persist_directory = persist_directory,
    embedding_function = embedding
)

if __name__ == "__main__":

    while True:
        
        query = input("user: ")
        
        if query == 'exit':
            break

        questions = loaded_vectordb.similarity_search(query,k=3)

        question = random.choice(questions)

        print(question.page_content,'\n')

    print('exit Qbot')
    exit(0)