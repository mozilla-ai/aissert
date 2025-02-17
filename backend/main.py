from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from llm import query_llm

app = FastAPI()

# Allow CORS so that the Vue frontend (which may be served on another port) can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(chat: ChatMessage):
    # Call our LLM query method using the provided prompt
    answer = query_llm(chat.message)
    return {"response": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
