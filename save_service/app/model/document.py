from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class Document(BaseModel):
    id: Optional[UUID] = uuid4()
    owner_id: UUID
    title: str
    body: str