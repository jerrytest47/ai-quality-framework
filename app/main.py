
import os

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

from app.policies import STORE_POLICIES

app = FastAPI(title="Northstar AI Support")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
    )

    response = client.responses.create(
        model=os.getenv(
            "OPENAI_MODEL",
            "gpt-4.1-mini"
        ),
        instructions=(
            "You are a customer support assistant "
            "for Northstar Electronics. "
            "Answer questions using only these "
            "store policies:\n"
            f"{STORE_POLICIES}\n"
            "If the policies do not answer the "
            "question, say you do not know. "
            "Never invent store policies."
        ),
        input=request.message,
    )

    return ChatResponse(
        answer=response.output_text
    )
