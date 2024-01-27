from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID
from model.document import Document
import uvicorn
import os

app = FastAPI()

db: List[Document] = [
    Document(owner_id=1,
             title="Title",
             body="testtext")
]


@app.get("/health", status_code=status.HTTP_200_OK)
async def doc_health():
    return {'message': 'service is active'}


@app.get("/user_docs")
async def fetch_docs():
    return db


@app.get("/doc_by_id")
async def fetch_docs(doc_id: int):
    for doc in db:
        if doc.owner_id == doc_id:
            return doc
    raise HTTPException(
        status_code=404,
        detail=f'Document with {doc_id} does not exist'
    )


@app.post('/add_doc')
async def add_doc(doc: Document):
    db.append(doc)
    return {"id": doc.id}

@app.delete('delete_doc')
async def delete_doc(doc_id: UUID):
    for doc in db:
        if doc.id == doc_id:
            db.remove(doc)
            return
    raise HTTPException(
        status_code=404,
        detail=f'Document with {doc_id} does not exist'
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))