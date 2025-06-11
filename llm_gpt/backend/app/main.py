import os
import sys
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Load env vars
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY not found in .env file")
    sys.exit(1)

# === App setup ===
app = FastAPI()
persist_directory = 'db'
vector_db = None
qa = None

# === Load docs and setup QA chain once ===
print(">>> Checking if document exists:", os.path.exists('./docs/document.txt'))
print(">>> Preparing documents and vector DB...")
loader = UnstructuredFileLoader('./docs/document.txt')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
split_texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vector_db = Chroma.from_documents(documents=split_texts, embeddings=embeddings, persist_directory=persist_directory)

chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
qa = RetrievalQA.from_chain_type(llm=chat_model, chain_type="stuff", retriever=vector_db.as_retriever())

print(">>> App setup complete.")

@app.get("/")
async def welcome(request: Request):
    return "Welcome to the LLM-GPT Demo"

@app.post("/")
async def generate_response(request: Request):
    request_data = await request.json()
    user_input = request_data['user_input']

    bot_response = qa.run(user_input)
    created_time = int(time.time())

    return JSONResponse(content={
        "created": created_time,
        "model": "llm-gpt-demo-v1",
        "content": bot_response
    })


