import os
import random
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

from openai import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

os.environ['TOKENIZERS_PARALLELISM']= 'False'

# create embedding
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Load chromadb langchain
persist_directory = './chroma/'
loaded_vectordb = Chroma(
    persist_directory = persist_directory,
    embedding_function = embedding
)

# load OPENAI_API_KEY
top_p = 1
temperature = 0.4
max_tokens = 100
model_name = 'gpt-3.5-turbo'
openai_api_key_path = '/home/loc/Documents/OPENAI_API_KEY.txt'

with open(openai_api_key_path) as f:
    OPENAI_API_KEY = f.read().strip()
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

client = OpenAI()

if __name__ == "__main__":

    while True:
        
        query = input("user: ")
        
        if query.strip() == 'exit':
            break

        else:
            # Retrieve question
            questions = loaded_vectordb.similarity_search(query,k=3)
            question = random.choice(questions)
            print(question.page_content,'\n')

            option = input('Yes for get answer, No for other question [y/n]: ')

            if option.lower() == 'y':

                # Prompt
                system_message = '''
                You are helpful assistant.Your mission is answer the question related to AWS services.
                The answer must base on the question, if the question is not related to AWS services.
                You will say sorry and ask for the other question.
                '''
                
                prompt = f'''
                Answer the question delimited by the triple backticks
                ```{question}```
                '''

                messages = [{'role':'system','content':system_message},
                {'role':'user','content':prompt}
                ]
                
                # Give the answer
                responses = client.chat.completions.create(
                model = model_name,
                messages = messages,
                max_tokens = max_tokens,
                temperature = temperature,
                top_p = top_p
                )

                print('answer:',responses.choices[0].message.content)
            else:
                pass

    print('exit Abot')
    exit(0)