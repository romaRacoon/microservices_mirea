from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from uuid import UUID
from model.document import Document
import uvicorn
import os
from database import database as database
from sqlalchemy.orm import Session

app = FastAPI()

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def doc_health():
    return {'message': 'service is active'}


@app.get("/user_docs")
async def fetch_docs(db: db_dependency):
    result = db.query(database.DBDoc).offset(0).limit(100).all()
    return result


@app.get("/doc_by_id/{owner_id}")
async def fetch_docs(owner_id: UUID, db: db_dependency):
    result = db.query(database.DBDoc).filter(database.DBDoc.owner_id == owner_id).first()
    print(owner_id)
    print(result)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'doc with such owner id is not found. owner_id: {owner_id}'
        )
    return result


@app.post('/add_doc')
async def add_doc(doc: Document, db: db_dependency):
    db_doc = database.DBDoc(
        id=doc.id,
        owner_id=doc.owner_id,
        title=doc.title,
        body=doc.body,
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return {"id": doc.id}


# @app.delete('delete_doc')
# async def delete_doc(doc_id: UUID):
#     for doc in db:
#         if doc.id == doc_id:
#             db.remove(doc)
#             return
#     raise HTTPException(
#         status_code=404,
#         detail=f'Document with {doc_id} does not exist'
#     )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
