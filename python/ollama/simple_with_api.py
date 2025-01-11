from langchain_ollama import ChatOllama

model = ChatOllama(
    model="llama3.2",
    temperature=0,
)


def get_response(message):
    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to Indonesian. Translate the user sentence.",
        ),
        ("human", message),
    ]
    model.invoke(messages)

    response = ''
    for chunk in model.stream(messages):
        response = response + chunk.content

    return response


from pydantic import BaseModel
from fastapi import FastAPI

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
    return get_response(item.message)
