# pdf loader
from langchain_community.document_loaders import PyPDFLoader

file_path = (
    "doc.pdf"
)
loader = PyPDFLoader(file_path)
docs = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)
all_splits = text_splitter.split_documents(docs)

from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3.2")

from langchain_chroma import Chroma

vector_store = Chroma(embedding_function=embeddings)
vector_store.add_documents(all_splits)

from langchain import hub
prompt = hub.pull("rlm/rag-prompt")

from langchain_ollama import ChatOllama

def get_response(message):
    llm = ChatOllama(
        model="llama3.2",
        temperature=0,
    )

    question = message

    retrieved_docs = vector_store.similarity_search(question)
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    invoke = prompt.invoke({"question": question, "context": docs_content})
    answer = llm.invoke(invoke)
    return answer.content

from pydantic import BaseModel
from fastapi import FastAPI

# How to run the api
# cd python/ollama
# uvicorn rag_with_api:app --reload

# Create a FastAPI instance
app = FastAPI()

# Define a route

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return get_response('I love programming')


class Item(BaseModel):
    message: str

@app.post("/ai_response/")
def create_item(item: Item):
    print(item.message)
    return get_response(item.message)
