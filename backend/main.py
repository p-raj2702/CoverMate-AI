# backend/main.py

from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from query import process_query

app = FastAPI()

class QueryInput(BaseModel):
    documents: str
    questions: list[str]

@app.post("/api/v1/hackrx/run")
async def run_query(payload: QueryInput, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Bearer token")

    answers = process_query(payload.documents, payload.questions)
    return {"answers": answers}