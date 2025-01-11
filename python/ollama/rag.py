# csv loader
from langchain_community.document_loaders.csv_loader import CSVLoader
import os

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = os.getcwd()

if '__file__' in globals():
    csv_path = os.path.join(base_dir, '..', 'python\\ollama\\SaleData.csv')
else:
    csv_path = os.path.join(base_dir, 'python\\ollama\\SaleData.csv')
        
loader = CSVLoader(file_path=csv_path)


# pdf loader
from langchain_community.document_loaders import PyPDFLoader

file_path = (
    "../doc.pdf"
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

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

question = "Sebutkan salah satu strategi pertahanan negara?"

retrieved_docs = vector_store.similarity_search(question)
docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
invoke = prompt.invoke({"question": question, "context": docs_content})
answer = llm.invoke(invoke)
print(answer)