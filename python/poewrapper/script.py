from pydantic import BaseModel
from fastapi import FastAPI
from poe_api_wrapper import AsyncPoeApi
import asyncio

tokens = {
    'p-b': 'Sdi1Gn_1sRNXadyaLxOOAg%3D%3D',
    'p-lat': 'YjeSj5B98kgtYCI2jpVdZgi4TvOm8vlgT2cAkLdxgQ%3D%3D',
}


async def get_poe_response(message):
    client = await AsyncPoeApi(tokens=tokens).create()
    response = ''
    chat_id = 0
    async for chunk in client.send_message(bot="BotUOXPYQEOOK", message=message):
        response = response + chunk["response"]
        chat_id = chunk['chatId']
    return {'response': response, 'chat_id': chat_id}


# Create a FastAPI instance
app = FastAPI()

# Define a route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    resp = asyncio.run(get_poe_response('Apa yang kamu ketahui'))
    return resp['response']


class Item(BaseModel):
    message: str

@app.post("/poe/")
def create_item(item: Item):
    resp = asyncio.run(get_poe_response('Apa yang kamu ketahui'))
    return resp
