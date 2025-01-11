from langchain_ollama import ChatOllama

model = ChatOllama(
    model="llama3.2",
    temperature=0,
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Indonesian. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
model.invoke(messages)

for token in model.stream(messages):
    print(token.content, end="|")