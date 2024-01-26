from fastapi import FastAPI, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
import database.database as database
import uvicorn
import os
import json
from uuid import UUID

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


@app.get("/fetch_docs_by_user")
async def fetch_docs(user_id: UUID, file_name: str, db: db_dependency):
    result = db.query(database.DBDoc).offset(0).limit(100).all()
    result_json = json.dumps([doc.__dict__ for doc in result], default=str, indent=2)

    with open(f"{file_name}.json", "w") as file:
        file.write(result_json)

    return {"message": f"Результаты успешно записаны в файл {file_name}.json"}
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
