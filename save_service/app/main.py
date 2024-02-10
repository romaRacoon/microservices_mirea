from fastapi import FastAPI, Depends, status, HTTPException, Header, Form
from typing import Annotated
from sqlalchemy.orm import Session
import database.database as database
import uvicorn
import os
import json
from uuid import UUID
from keycloak import KeycloakOpenID

#Инициализация фастапи
app = FastAPI()

#Работа с БД
database.Base.metadata.create_all(bind=database.engine)

# Данные для подключения к Keycloak
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "artemenkov"
KEYCLOAK_REALM = "myrealm"
KEYCLOAK_CLIENT_SECRET = "Sd0kf6dI8mZNBULCJjGUAbcioNK7wCbM"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_token = ""
@app.post("/get-token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def check_user_roles():
    global user_token
    token = user_token
    try:
        userinfo = keycloak_openid.userinfo(token["access_token"])
        token_info = keycloak_openid.introspect(token["access_token"])
        if "testRole" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def doc_health():
    # print(check_user_roles())
    if (check_user_roles()):
        return {'message': 'service is active'}
    else:
        return "something went wrong"


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
